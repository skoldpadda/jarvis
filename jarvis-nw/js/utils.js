var path = require('path'),
    os = require('os');

var utils = {};

utils.getUserHome = function() {
    return process.env.HOME || process.env.HOMEPATH || process.env.USERPROFILE;
};

utils.getUserName = function() {
    return os.hostname().split('.').shift();
};

utils.userRequire = function(filepath) {
    return require(path.resolve(this.getUserHome(), 'jarvis-data', filepath));
};

module.exports = utils;