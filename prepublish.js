var exec = require('child_process').exec,
    path = require('path');

var rootdir = process.cwd();

function runExec(dir, command, then) {
    process.chdir(path.resolve(rootdir, dir));
    exec(command, {'cwd': process.cwd()}, function(error, stdout, stderr) {
        console.log("stdout: " + stdout);
        console.log("stderr: " + stderr);
        if (error !== null) {
            console.log("PREPUBLISH ERROR: " + error);
        }
        if (then) {
            then();
        }
    });
}

runExec('kernel', 'python bootstrap.py', function() {
    runExec('jarvis-nw', 'npm install');
});