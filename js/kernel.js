var events = require('events');

function Kernel() {
    events.EventEmitter.call(this);
}

Kernel.prototype.__proto__ = events.EventEmitter.prototype;

Kernel.prototype.userInput = function(input) {
    var self = this;

    // @TODO: should it really be printed out in all cases?
    self.emit('user_input_acknowledged', input);

    return self;
}

module.exports = Kernel;