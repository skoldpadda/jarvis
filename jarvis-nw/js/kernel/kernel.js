var os = require('os'),
    fs = require('fs-extra'),
    util = require('util'),
    events = require('events'),
    path = require('path');

// External libraries
var moment = require('../lib/moment.js');

var utils = require('./utils.js');

// @TODO: aliases?
var builtins = require('./builtins.js');


/** KERNEL DEFINITION **/

function Kernel() {
    events.EventEmitter.call(this);
}

util.inherits(Kernel, events.EventEmitter);






Kernel.prototype.boot = function() {
    // @TODO: Load settings and user folder, if it doesn't exist make it.
    var u = path.resolve(utils.getUserHome(), 'jarvis-data');

    if (!fs.existsSync(u)) {
        fs.copySync('./js/user', u);
    }
    
};

Kernel.prototype.postInit = function() {
    this.jarvisMessage("Starting up on " + moment().format('MMMM Do YYYY, h:mm:ss a'));
};


Kernel.prototype.jarvisMessage = function(message) {
    this.emit('message', {"author": "jarvis", "tag": "jarvis > ", "text": message + "\n"});
};

Kernel.prototype.userMessage = function(message) {
    this.emit('message', {"author": "user", "tag": os.hostname() + " > ", "text": message + "\n"});
};


Kernel.prototype.userInput = function(input) {
    var self = this;

    // @TODO: should it really be printed out in all cases?
    self.userMessage(input);

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

    // Close?
    if (['exit', 'quit', 'bye'].indexOf(cmd) > -1) {
        self.emit('trigger_close');
        return;
    }


    // Where cmd is a string
    if (cmd in builtins && typeof builtins[cmd] === "function") {
        self.emit('kernel_out', builtins[cmd](args));
        return;
    }

    // @TODO: Consider, is try-catching errant input too expensive?
    try {
        var script = utils.userRequire("scripts/" + cmd);
        self.emit('kernel_out', script.run(args));
        return;
    } catch (err) {
        //console.log(err);
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
};

module.exports = Kernel;