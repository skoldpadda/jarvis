var events = require('events');
var cp = require('child_process');
var path = require('path');

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


/**
 * require()'s a path relative to the user/ directory.
 *
 * NOTE: Terrible hackity hack hack.
 * The cwd for a packaged app is in a temporary folder, so we have to break out of the executable using process.execPath.
 *
 * Unbuilt: jarvis\node_modules\nodewebkit\nodewebkit\nw.exe
 * Built:   jarvis\dist\releases\jarvis\win\jarvis\jarvis.exe
 * 
 * So we can place the user/ folder:
 * Unbuilt: jarvis\
 * Built:   jarvis\dist\releases\
 *
 * And then require it with the path below. (IS THIS BAD YES)
 *
 * @TODO: More realistically, we should have a bundled user/ folder which we copy to a reliable directory, such as
 * that returned by getUserHome(), if it doesn't already exist. This would only have to be done once (or whenever
 * the user decides to purge their config).
 */
Kernel.prototype.userRequire = function(filepath) {
    return require(path.resolve(process.execPath, "../../../../user/" + filepath));
}

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

    try {
        var script = self.userRequire("scripts/" + cmd);
        self.emit('kernel_out', script.run(args));
        return;
    } catch (err) {
        console.log(err);
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