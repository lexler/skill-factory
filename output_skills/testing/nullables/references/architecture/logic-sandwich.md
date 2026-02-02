# Logic Sandwich

Application layer code follows a consistent pattern: read from infrastructure, process with pure logic, write to infrastructure.

```
READ    → Get data from Infrastructure
PROCESS → Transform with Logic (pure functions)
WRITE   → Send results to Infrastructure
```

The "meat" (logic) is sandwiched between "bread" (I/O). This keeps logic pure and testable.

## Example

```javascript
class OrderProcessor {
  constructor(database, emailer, logger) {
    this._db = database;
    this._emailer = emailer;
    this._logger = logger;
  }

  async processOrder(orderId) {
    // READ
    const order = await this._db.getOrder(orderId);
    const inventory = await this._db.getInventory(order.items);

    // PROCESS (pure logic)
    const result = OrderLogic.validate(order, inventory);
    const confirmation = OrderLogic.createConfirmation(result);

    // WRITE
    await this._db.updateOrder(orderId, result.status);
    await this._emailer.send(confirmation);
    this._logger.info("Order processed", { orderId, status: result.status });
  }
}
```

## Testing

Null the infrastructure, verify the writes:

```javascript
it("sends confirmation email for valid order", async () => {
  const db = Database.createNull({
    order: { id: "123", items: ["widget"] },
    inventory: { widget: 10 }
  });
  const emailer = Emailer.createNull();
  const emails = emailer.trackOutput();
  const logger = Logger.createNull();

  const processor = new OrderProcessor(db, emailer, logger);
  await processor.processOrder("123");

  assert.equal(emails.data.length, 1);
  assert.equal(emails.data[0].subject, "Order Confirmed");
});
```

Notice: the test creates Nullables for all infrastructure, runs real application code, and verifies outcomes via Output Tracking.

## Multiple Reads or Writes

The pattern extends naturally:

```javascript
async transferFunds(fromId, toId, amount) {
  // READ (multiple)
  const from = await this._accounts.get(fromId);
  const to = await this._accounts.get(toId);
  const rate = await this._exchange.getRate(from.currency, to.currency);

  // PROCESS
  const transfer = TransferLogic.calculate(from, to, amount, rate);
  if (!transfer.valid) throw new Error(transfer.reason);

  // WRITE (multiple)
  await this._accounts.debit(fromId, transfer.fromAmount);
  await this._accounts.credit(toId, transfer.toAmount);
  this._audit.log("transfer", transfer);
}
```

## When Logic Gets Complex

If PROCESS becomes complex, extract it to a Logic module:

```javascript
// application layer - thin
async processOrder(orderId) {
  const order = await this._db.getOrder(orderId);
  const result = OrderLogic.process(order);  // all logic here
  await this._db.save(result);
}

// logic layer - pure, easily tested
class OrderLogic {
  static process(order) {
    const validated = this.validate(order);
    const priced = this.calculatePricing(validated);
    const confirmed = this.createConfirmation(priced);
    return confirmed;
  }
}
```

Logic layer tests don't need Nullables at all - just call the pure functions.
