self.addEventListener("install", event => {
  event.waitUntil(self.skipWaiting());
});

self.addEventListener("activate", event => {
  event.waitUntil(self.clients.claim());
});

function getJSON(data) {
  var result = {
    ok: false,
  };
  try {
    result.value = data.json();
    result.ok = true;
  } catch (e) {
    // Ignore syntax errors for invalid JSON.
  }
  return result;
}

function assert(value, message) {
  if (!value) {
    throw new Error(message);
  }
}

function broadcast(event, promise) {
  event.waitUntil(Promise.resolve(promise).then(message => {
    return self.clients.matchAll().then(clients => {
      clients.forEach(client => client.postMessage(message));
    });
  }));
}

function reply(event, promise) {
  event.waitUntil(Promise.resolve(promise).then(result => {
    event.ports[0].postMessage(result);
  }).catch(error => {
    event.ports[0].postMessage({
      error: String(error),
    });
  }));
}

self.addEventListener("push", event => {
  var message = {
    type: event.type,
    ok: true,
  };
  if (event.data) {
    message.data = {
      text: event.data.text(),
      arrayBuffer: event.data.arrayBuffer(),
      json: getJSON(event.data),
      blob: event.data.blob(),
    };
  }
  broadcast(event, message);
});

var testHandlers = {
  publicKey(data) {
    return self.registration.pushManager.getSubscription().then(
      subscription => ({
        p256dh: subscription.getKey("p256dh"),
        auth: subscription.getKey("auth"),
      })
    );
  },

  resubscribe(data) {
    return self.registration.pushManager.getSubscription().then(
      subscription => {
        assert(subscription.endpoint == data.endpoint,
          "Wrong push endpoint in worker");
        return subscription.unsubscribe();
      }
    ).then(result => {
      assert(result, "Error unsubscribing in worker");
      return self.registration.pushManager.getSubscription();
    }).then(subscription => {
      assert(!subscription, "Subscription not removed in worker");
      return self.registration.pushManager.subscribe();
    }).then(subscription => {
      return {
        endpoint: subscription.endpoint,
      };
    });
  },

  subscribeWithKey(data) {
    return self.registration.pushManager.subscribe({
      applicationServerKey: data.key,
    }).then(subscription => {
      return {
        endpoint: subscription.endpoint,
        key: subscription.options.applicationServerKey,
      };
    }, error => {
      return {
        isDOMException: error instanceof DOMException,
        name: error.name,
      };
    });
  },
};

self.addEventListener("message", event => {
  var handler = testHandlers[event.data.type];
  if (handler) {
    reply(event, handler(event.data));
  } else {
    reply(event, Promise.reject(
      "Invalid message type: " + event.data.type));
  }
});

self.addEventListener("pushsubscriptionchange", event => {
  broadcast(event, {
    type: event.type,
    ok: true,
  });
});
