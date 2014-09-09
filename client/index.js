var node_static = require('node-static');


var client = {};

client.staticServer = new node_static.Server(__dirname + "/dist");

module.exports = client;
