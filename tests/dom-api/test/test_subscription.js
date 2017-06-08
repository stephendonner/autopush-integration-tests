describe("A push subscription", () => {
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

  it("should provide a serializer", () => co(function*() {
    var json = pushSubscription.toJSON();
    assert.equal(json.endpoint, pushSubscription.endpoint, "Wrong endpoint");

    ["p256dh", "auth"].forEach(keyName => {
      assert.deepEqual(
        base64URLDecode(json.keys[keyName]),
        new Uint8Array(pushSubscription.getKey(keyName)),
        "Mismatched Base64-encoded key: " + keyName
      );
    });
  }));

  it("should be exposed to the service worker", () => co(function*() {
    var data = yield sendRequestToController({ type: "publicKey" });

    var p256dhKey = new Uint8Array(pushSubscription.getKey("p256dh"));
    assert.equal(p256dhKey.length, 65, "Key share should be 65 octets");
    assert.deepEqual(p256dhKey, new Uint8Array(data.p256dh),
      "Mismatched key share");

    var authSecret = new Uint8Array(pushSubscription.getKey("auth"));
    assert.equal(authSecret.length, 16, "Auth secret should be 16 octets");
    assert.deepEqual(authSecret, new Uint8Array(data.auth),
      "Mismatched auth secret");
  }));
});
