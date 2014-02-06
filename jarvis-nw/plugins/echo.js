// @TODO: Doesn't work. See kernel.js

process.on('message', function(args) {
    process.stdout.write(args + "\n");
});