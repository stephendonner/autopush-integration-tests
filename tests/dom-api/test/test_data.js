describe("A push message", () => {
  var assert = chai.assert;

  var registration;
  var pushSubscription;
  before(() => co(function*() {
    var url = "worker.js?" + Math.random();
    registration = yield navigator.serviceWorker.register(url, { scope: "." });
    pushSubscription = yield registration.pushManager.subscribe();
  }));

  after(() => co(function*() {
    yield pushSubscription.unsubscribe();
    yield registration.unregister();
  }));

  it("can be a text string", () => co(function*() {
    var message = yield waitForPush(pushSubscription, "Text message from page");
    assert.equal(message.data.text, "Text message from page",
      "Wrong text message data");
  }));

  it("can be a typed array", () => co(function*() {
    var typedArray = new Uint8Array([226, 130, 40, 240, 40, 140, 188]);
    var message = yield waitForPush(pushSubscription, typedArray);
    assert.deepEqual(new Uint8Array(message.data.arrayBuffer), typedArray,
      "Wrong array buffer message data");
  }));

  it("can be JSON", () => co(function*() {
    var json = { hello: "world" };
    var message = yield waitForPush(pushSubscription, JSON.stringify(json));
    assert(message.data.json.ok, "Unexpected error parsing JSON");
    assert.deepEqual(message.data.json.value, json, "Wrong JSON message data");
  }));

  it("can be empty", () => co(function*() {
    var message = yield waitForPush(pushSubscription, "");
    assert(message, "Should include data for empty messages");
    assert.strictEqual(message.data.text, "", "Wrong text for empty message");
    assert.strictEqual(message.data.arrayBuffer.byteLength, 0,
      "Wrong buffer length for empty message");
    assert.notOk(message.data.json.ok,
      "Expected JSON parse error for empty message");
  }));

  var withAstralSymbol = new Uint8Array(
    [0x48, 0x69, 0x21, 0x20, 0xf0, 0x9f, 0x91, 0x80]);
  it("can include astral symbols", () => co(function*() {
    var message = yield waitForPush(pushSubscription, withAstralSymbol);
    assert.equal(message.data.text, "Hi! \ud83d\udc40",
      "Wrong text for message with emoji");
  }));

  it("can be a blob", () => co(function*() {
    var message = yield waitForPush(pushSubscription, withAstralSymbol);
    var text = yield new Promise((resolve, reject) => {
      var reader = new FileReader();
      reader.onloadend = event => {
        if (reader.error) {
          reject(reader.error);
        } else {
          resolve(reader.result);
        }
      };
      reader.readAsText(message.data.blob);
    });
    assert.equal(text, "Hi! \ud83d\udc40",
      "Wrong blob data for message with emoji");
  }));

  it("can be null if omitted", () => co(function*() {
    var promiseMessage = waitOnController("push");
    var response = yield fetch(pushSubscription.endpoint, {
      method: "POST",
      headers: { ttl: "120" },
    });
    assert.equal(response.status, 201, "Wrong status code for blank message");
    var message = yield promiseMessage;
    assert.notOk(message.data, "Should exclude data for blank messages");
  }));

  it("can include additional padding", () => co(function*() {
    var promiseMessage = waitOnController("push");
    yield webpush(pushSubscription, {
      payload: "This is a padded message",
      ttl: 60,
      paddingBytes: 512
    });
    var message = yield promiseMessage;
    assert.equal(message.data.text, "This is a padded message",
      "Wrong text for padded message");
  }));
});
