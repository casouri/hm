var request = require("request");
var Service, Characteristic;
var fs = require('fs');

module.exports = function(homebridge) {
    Service = homebridge.hap.Service;
    Characteristic = homebridge.hap.Characteristic;

    // plugin name, display name, plugin
    homebridge.registerAccessory("homebridge-http-switch", "http-switch", HTTPSSwitchAccessory);
}

function HTTPSSwitchAccessory(log, config) {
    this.log = log;
    this.name = config["name"];
    this.password = config["password"];
    this.port = config["port"];

    this.service = new Service.Switch(this.name);

    this.service.getCharacteristic(Characteristic.On)
        .on('get', this.getState.bind(this))
        .on('set', this.setState.bind(this));
}

HTTPSSwitchAccessory.prototype.getState = function(callback) {
    this.log('Getting current state');

    request.post({
        url: 'http://localhost:%d' %this.port,
        form: {'action': 'get-status', 'accessory-name': this.name, 'passwd': this.password}
    }, function(err, response, body) {
        if (!err && response.statusCode == 200) {
            this.log("got state");
            callback(null, "on");
            // TODO: return real state
        }
        else {
            this.log("Error '%s' setting switch state. Response: %s", err, body);
            callback(err || new Error("Error setting switch state."));
        }
    }.bind(this));
};

HTTPSSwitchAccessory.prototype.setState = function(state, callback) {
  var HTTPSSwitchState = state ? "on": "off";
    var actionToTake = state ? "switch-off" : "switch-on";

  this.log("Set state to %s", HTTPSSwitchState);

    request.post({
        url: 'http://localhost:%d' %this.port,
        form: {'action': actionToTake, 'accessory-name': this.name, 'passwd': this.password}
    }, function(err, response, body) {
        if (!err && response.statusCode == 200) {
            this.log("State change complete.");


            // TODO: make sure state actually changes
            // this.service
            //     .setCharacteristic(Characteristic.On, state);

            callback(null, state); // success
        }
        else {
            this.log("Error '%s' setting lock state. Response: %s", err, body);
            callback(err || new Error("Error setting lock state."));
        }
    }.bind(this));

}

HTTPSSwitchAccessory.prototype.getServices = function() {
    return [this.service];
}
