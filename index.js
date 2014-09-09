var http = require('http');

var kernel = require('./kernel'),
	client = require('./client');


var server = http.createServer();

server.addListener('request', function(req, res) {
	client.staticServer.serve(req, res);
});

kernel.socket.install(server, '/kernel');

console.log('jarvis up and running!');
server.listen(8080);
