# Event-Driven Code

For event-driven applications (WebSockets, message queues, real-time systems), use the Traffic Cop pattern with Behavior Simulation.

## Traffic Cop

An observer that routes each event to its own Logic Sandwich:

```javascript
class ChatServer {
  constructor(network, database, logger) {
    this._network = network;
    this._db = database;
    this._logger = logger;
  }

  start() {
    this._network.on("connection", (client) => this._handleConnection(client));
    this._network.on("message", (client, msg) => this._handleMessage(client, msg));
    this._network.on("disconnect", (client) => this._handleDisconnect(client));
  }

  // Each handler is a Logic Sandwich
  async _handleMessage(client, rawMessage) {
    // READ
    const user = await this._db.getUser(client.userId);

    // PROCESS
    const message = ChatLogic.formatMessage(user, rawMessage);
    const recipients = ChatLogic.findRecipients(message, this._clients);

    // WRITE
    for (const recipient of recipients) {
      this._network.send(recipient, message);
    }
    this._logger.info("Message sent", { from: user.name, to: recipients.length });
  }
}
```

The "cop" directs traffic to handlers. Each handler follows Logic Sandwich.

## Behavior Simulation

To test event-driven code, add `simulateX()` methods to your Nullables:

```javascript
class Network {
  static create() {
    return new Network(new RealSocket());
  }

  static createNull() {
    return new Network(new StubbedSocket());
  }

  constructor(socket) {
    this._socket = socket;
    this._handlers = {};
  }

  // Real event handling
  on(event, handler) {
    this._handlers[event] = handler;
  }

  // Behavior simulation - uses same handlers
  simulateConnection(clientId, data) {
    this._handlers["connection"]?.({ id: clientId, ...data });
  }

  simulateMessage(clientId, message) {
    this._handlers["message"]?.(clientId, message);
  }

  simulateDisconnect(clientId) {
    this._handlers["disconnect"]?.(clientId);
  }
}
```

Key insight: `simulateX()` methods call the same handlers as real events. This ensures tests exercise the real code path.

## Testing with Behavior Simulation

```javascript
it("broadcasts messages to other clients", async () => {
  const network = Network.createNull();
  const sent = network.trackOutput();
  const db = Database.createNull({ user: { name: "Alice" } });
  const logger = Logger.createNull();

  const server = new ChatServer(network, db, logger);
  server.start();

  // Simulate events
  network.simulateConnection("client-1", { userId: "alice" });
  network.simulateConnection("client-2", { userId: "bob" });
  network.simulateMessage("client-1", "Hello!");

  assert.deepEqual(sent.data, [
    { to: "client-2", message: { from: "Alice", text: "Hello!" } }
  ]);
});
```

## Avoid

- **God Classes** - Keep each handler focused on one responsibility
- **Complex handlers** - Extract logic to Logic layer if handlers grow
- **Untested event paths** - Simulate all event types in tests
