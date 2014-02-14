var path = require('path');

var utils = {};

utils.getUserHome = function() {
    return process.env.HOME || process.env.HOMEPATH || process.env.USERPROFILE;
};

utils.userRequire = function(filepath) {
    return require(path.resolve(this.getUserHome(), "jarvis-data", filepath));
};

module.exports = utils;