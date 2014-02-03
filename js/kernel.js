var events = require('events');
var cp = require('child_process');

/** BUILT-IN SCRIPTS **/
// @TODO: aliases?
// @TODO: should this even be here? more consistent to also make them modules. but also less secure.

var builtins = {};

builtins.help = function(args) {
    return "help";
};

builtins.history = function(args) {
    return "history";
};

builtins.cd = function(args) {
    //
};


/** KERNEL DEFINITION **/

function Kernel() {
    events.EventEmitter.call(this);
}

Kernel.prototype.__proto__ = events.EventEmitter.prototype;

Kernel.prototype.userInput = function(input) {
    var self = this;

    // @TODO: should it really be printed out in all cases?
    self.emit('user_input_acknowledged', input);

    if (!input) {
        return;
    }

    /**
     * 1. Is it a built-in function? (right in this class)
     * 2. Is it a script in plugins/ folder (recursive)?
     * 3. Is it a native shell command?
     * 4. Pass to semantic analyzer
     */

    // @TODO: This is horrible hack
    var parsed = input.match(/(?:[^\s"]+|"[^"]*")+/g);
    var cmd = parsed[0];
    var args = parsed.slice(1);

    // Where cmd is a string
    if (cmd in builtins && typeof builtins[cmd] === "function") {
        self.emit('kernel_out', builtins[cmd](args));
        return;
    }


    /** So it turns out fork() is broken in node-webkit. This is a bummer. https://github.com/rogerwang/node-webkit/issues/213
     * Not that we'd really NEED async second-process execution though? I mean it's cleaner...
     * but in the Jarvis model in -> out makes just as much sense.
     * Possible workaround: https://gist.github.com/iamkvein/2006752
     * Basically, we implement our own common abstraction, or perhaps intercept process.stdout/stderr.
    var child = cp.fork("./plugins/" + cmd);
    child.stdout.on('data', function(data) {
        console.log('stdout: ' + data);
    });
    child.send(args);
    */


    self.emit('kernel_err', "Unrecognized command \"" + cmd + "\"");

    return self;
}

module.exports = Kernel;