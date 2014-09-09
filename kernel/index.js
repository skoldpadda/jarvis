var shoe = require('shoe-bin');


var kernel = {};

kernel.socket = shoe(function(stream) {
	stream.on('data', function(message) {
		stream.write(message);
	});
});

module.exports = kernel;
