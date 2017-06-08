'use strict';

var assert = require('assert');
var http = require('http');
var url = require('url');

var P = require('bluebird');
var express = require('express');

// A helper that sets permissions for a given origin.
function setPermissions(client, origin, permissions) {
  var chrome = client.scope({
    context: 'chrome',
  });
  // Marionette serializes and executes the `chromeScript` function in the
  // parent Firefox process.
  var p = chrome.executeScript(function chromeScript(origin, permissions) {
    var Cc = Components.classes;
    var Ci = Components.interfaces;

    var permissionManager = Cc["@mozilla.org/permissionmanager;1"].
                              getService(Ci.nsIPermissionManager);
    var scriptSecurityManager = Cc["@mozilla.org/scriptsecuritymanager;1"].
                                  getService(Ci.nsIScriptSecurityManager);

    var principal =
      scriptSecurityManager.createCodebasePrincipalFromOrigin(origin);

    for (var type in permissions) {
      if (permissions[type]) {
        permissionManager.addFromPrincipal(principal, type,
          Ci.nsIPermissionManager.ALLOW_ACTION);
      } else {
        permissionManager.removeFromPrincipal(principal, type);
      }
    }
  }, [origin, permissions]);
}

marionette('Autopush integration test', function testIntegration() {
  // Set up a static file server to host our tests.
  var app = express();
  app.use(express.static(__dirname + '/test'));

  var server = http.createServer(app);
  var serverURL;

  var client = marionette.client({
    // Use the async driver. The default driver is synchronous and will block
    // our test server from handling requests.
    driver: require('marionette-client').Drivers.Promises,
    profile: {
      prefs: {
        // The Autopush server URL.
        'dom.push.serverURL': 'wss://autopush.stage.mozaws.net',

        // Allow insecure origins to register service workers.
        'dom.serviceWorkers.testing.enabled': true,

        'dom.push.enabled': true,
        'dom.push.connection.enabled': true,
        'dom.serviceWorkers.exemptFromPerDomainMax': true,
        'dom.serviceWorkers.enabled': true,
      },
    },
  });

  // Starts the test server on a random port, then constructs the server URL and
  // enables notifications to avoid the permission doorhanger.
  setup(function setup() {
    return new P(function listenResolver(resolve) {
      server.listen(resolve);
    }).then(function handleListen() {
      var address = server.address();
      serverURL = url.format({
        protocol: 'http',
        hostname: address.address,
        port: address.port,
      });
      setPermissions(client, serverURL, {
        'desktop-notification': true,
      });
    });
  });

  teardown(function teardown() {
    // At this point, the client has already disconnected, so we can't send
    // any more commands to Firefox.
    return new P(function closeResolver(resolve) {
      server.close(resolve);
    });
  });

  // If we omit the options, Marionette defaults to `{ devices: ["phone"] }`,
  // which causes the runner to ignore our tests. We work around this by
  // passing an empty object.
  test('should test the DOM API', {}, function testDOMAPI() {
    return client.goUrl(serverURL).then(function handleGoUrl() {
      // The `contentScript` function is serialized and executed in the
      // content process.
      return client.executeAsyncScript(function contentScript() {
        document.addEventListener('testsDone', function onTestsDone(event) {
          document.removeEventListener('testsDone', onTestsDone);
          marionetteScriptFinished(event.detail);
        });
      });
    }).then(function handleExecute(result) {
      assert.deepEqual(result.value.failures, []);
    });
  });
});
