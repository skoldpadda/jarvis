process.chdir('./jarvis-nw');

var exec = require('child_process').exec,
    child;

child = exec('npm install', {'cwd': process.cwd()}, function(error, stdout, stderr) {
    console.log("stdout: " + stdout);
    console.log("stderr: " + stderr);
    if (error !== null) {
        console.log("PREPUBLISH ERROR: " + error);
    }
});