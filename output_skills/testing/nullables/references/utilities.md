# Utilities: OutputListener and ConfigurableResponses

Two tiny reusable classes carry the whole approach — one for the write channel, one for the read channel. Copy them into the codebase (e.g. `infrastructure/util/`) when it doesn't have them; they are production code and get committed like any other. JS and Java versions are below — in another language, port them, preserving the semantics stated with each (they are well under 100 lines apiece).

## OutputListener / OutputTracker

Wrappers hold an `OutputListener` and `emit(domainData)` at the moment of each write, in code shared by real and nulled paths. Tests call `trackX()` to get an `OutputTracker`. No tracker subscribed → emit is a no-op.

JavaScript/TypeScript:

```javascript
import { EventEmitter } from "node:events";

const EVENT = "output";

export class OutputListener {
  constructor() {
    this._emitter = new EventEmitter();
  }
  emit(data) {
    this._emitter.emit(EVENT, data);
  }
  trackOutput() {
    return new OutputTracker(this._emitter);
  }
}

class OutputTracker {
  constructor(emitter) {
    this._emitter = emitter;
    this._data = [];
    this._listener = (item) => this._data.push(item);
    this._emitter.on(EVENT, this._listener);
  }
  get data() {
    return this._data;
  }
  clear() {                       // return current data and reset
    const result = [...this._data];
    this._data.length = 0;
    return result;
  }
  stop() {                        // unsubscribe
    this._emitter.off(EVENT, this._listener);
  }
}
```

Java:

```java
public class OutputListener<T> {
    private final List<OutputTracker<T>> listeners = new ArrayList<>();

    public void emit(T data) {
        listeners.forEach(tracker -> tracker.add(data));
    }

    public OutputTracker<T> trackOutput() {
        OutputTracker<T> tracker = new OutputTracker<>(this);
        listeners.add(tracker);
        return tracker;
    }

    void remove(OutputTracker<T> outputTracker) {
        listeners.remove(outputTracker);
    }
}

public class OutputTracker<T> {
    private final List<T> output = new ArrayList<>();
    private final OutputListener<T> outputListener;

    public OutputTracker(OutputListener<T> outputListener) {
        this.outputListener = outputListener;
    }

    void add(T data) {
        output.add(data);
    }

    public List<T> data() {
        return List.copyOf(output);
    }

    public List<T> clear() {
        List<T> data = this.data();
        output.clear();
        return data;
    }

    public void stop() {
        outputListener.remove(this);
    }
}
```

Usage in a wrapper:

```java
private final OutputListener<Game.Snapshot> listener = new OutputListener<>();

public void saveGame(Game.Snapshot snapshot) {
    gameDatabaseJpa.save(GameRow.from(snapshot));
    listener.emit(snapshot);                    // domain-level, both modes
}
public OutputTracker<Game.Snapshot> trackSaves() {
    return listener.trackOutput();
}
```

## ConfigurableResponses

Encapsulates the read-channel semantics: a single value repeats forever; a list is consumed in order and then fails fast with a named error. Used inside embedded stubs.

JavaScript/TypeScript:

```javascript
export class ConfigurableResponses {
  // Array → different response each call, throws when exhausted.
  // Anything else → same response every call, never runs out.
  // 'name' appears in error messages.
  static create(responses, name) {
    return new ConfigurableResponses(responses, name);
  }

  // Convert every property of an object: { "/a": 1 } → { "/a": ConfigurableResponses }
  static mapObject(responseObject, name) {
    const entries = Object.entries(responseObject).map(([key, value]) => {
      const translatedName = name === undefined ? undefined : `${name}: ${key}`;
      return [key, ConfigurableResponses.create(value, translatedName)];
    });
    return Object.fromEntries(entries);
  }

  constructor(responses, name) {
    this._description = name === undefined ? "" : ` in ${name}`;
    this._responses = Array.isArray(responses) ? [...responses] : responses;
  }

  next() {
    const response = Array.isArray(this._responses)
      ? this._responses.shift()
      : this._responses;
    if (response === undefined) {
      throw new Error(`No more responses configured${this._description}`);
    }
    return response;
  }
}
```

Java idiom (iterator normalization):

```java
private static Iterator<Object> normalize(Object responses) {
    if (responses instanceof List) {
        return ((List<Object>) responses).iterator();       // in order, then hasNext() false
    }
    return Stream.generate(() -> responses).iterator();     // repeats forever
}

private Object next(String key, Iterator<Object> responses) {
    if (!responses.hasNext()) {
        throw new NoSuchElementException("No more responses configured for: " + key);
    }
    return responses.next();
}
```

Usage in a stub:

```javascript
class StubbedHttp {
  constructor(responses = {}) {
    this._responses = ConfigurableResponses.mapObject(responses, "nulled HTTP client");
  }
  request({ path }) {
    return new StubbedRequest(this._responses[path]?.next() ?? DEFAULT_NULLED_RESPONSE);
  }
}
```
