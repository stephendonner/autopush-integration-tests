function waitForPush(pushSubscription, payload) {
  var promiseMessage = waitOnController("push");
  return webpush(pushSubscription, {
    payload: payload,
    ttl: 60,
  }).then(() => promiseMessage);
}

function waitOnController(type) {
  return new Promise((resolve, reject) => {
    function onMessage(event) {
      if (event.data.type == type) {
        navigator.serviceWorker.removeEventListener("message", onMessage);
        (event.data.ok ? resolve : reject)(event.data);
      }
    }
    navigator.serviceWorker.addEventListener("message", onMessage);
  });
}

function sendRequestToController(request) {
  return new Promise((resolve, reject) => {
    var channel = new MessageChannel();
    channel.port1.onmessage = e => {
      (e.data.error ? reject : resolve)(e.data);
    };
    navigator.serviceWorker.controller.postMessage(request, [channel.port2]);
  });
}

function webpush(pushSubscription, options) {
  return co(function*() {
    var payload = ArrayBuffer.isView(options.payload) ?
      options.payload.buffer : options.payload;
    if (!Number.isFinite(options.ttl)) {
      throw new Error("Invalid TTL: " + options.ttl);
    }
    var paddingBytes = Number.isFinite(options.paddingBytes) ?
      options.paddingBytes : 0;

    var senderKeys = yield KeyPair.generate();
    var senderPublicKey = yield senderKeys.exportPublicKey();
    var receiverKeys = yield KeyPair.import(
      pushSubscription.getKey("p256dh"));
    var cryptographer = new WebPushCryptographer(senderKeys, receiverKeys,
      pushSubscription.getKey("auth"));

    var salt = crypto.getRandomValues(new Uint8Array(16));
    var ciphertext = yield cryptographer.encrypt(salt, payload, paddingBytes);

    var response = yield fetch(pushSubscription.endpoint, {
      method: "POST",
      headers: {
        "content-encoding": "aesgcm",
        "crypto-key": "keyid=p256dh;dh=" + base64URLEncode(senderPublicKey),
        encryption: "keyid=p256dh;salt=" + base64URLEncode(salt),
        ttl: options.ttl,
      },
      body: ciphertext,
    });
    if (!response.ok) {
      throw new Error("Error delivering message: " + response.status);
    }
    return response;
  });
}

function base64URLEncode(bufferSource) {
  var array = new Uint8Array(ArrayBuffer.isView(bufferSource) ?
    bufferSource.buffer : bufferSource);
  var string = btoa(String.fromCharCode.apply(null, array));
  return string.replace(/\+/g, "-").replace(/\//g, "_").replace(/=/g, "");
}

function base64URLDecode(input) {
  var string = input.replace(/-/g, "+").replace(/_/g, "/");
  if (string.length % 4 == 2) {
    string += "==";
  } else if (string.length % 4 == 3) {
    string += "=";
  }
  var binaryString = atob(string);
  var array = new Uint8Array(binaryString.length);
  for (var i = 0; i < binaryString.length; i++) {
    array[i] = binaryString.charCodeAt(i);
  }
  return array;
}
