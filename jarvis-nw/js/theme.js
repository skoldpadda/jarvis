var vein = require('./lib/vein.js');
var utils = require('./utils.js');

var theme = {};

var current_theme;

var colormap = {
    'red': 8,
    'orange': 9,
    'yellow': 10,
    'green': 11,
    'teal': 12,
    'blue': 13,
    'purple': 14,
    'brown': 15,

    'foreground': 0,
    'background': 7,
    'titlebar': 6,
};

var default_theme = {
    name: 'Default',
    author: 'William Gaul',
    colors: [
        '#1d1f21', '#282a2e', '#373b41', '#969896', '#b4b7b4', '#c5c8c6', '#e0e0e0', '#ffffff',
        '#c82829', '#f5871f', '#eab700', '#718c00', '#3e999f', '#4271ae', '#8959a8', '#a3685a'
    ]
};


theme.loadTheme = function(name) {
    try {
        current_theme = utils.userRequire("themes/" + name + ".js");
    } catch (err) {
        console.log("Could not load theme: " + name + err);
        // If a theme has not been loaded yet, default to [default_theme]
        if (typeof current_theme === 'undefined' || current_theme === null) {
            current_theme = default_theme;
        }
    }
};

theme.color = function(color) {
    if (typeof color === 'string') {
        // @TODO: Suppose it doesn't exist in [colormap]?
        color = colormap[color];
    }
    return current_theme.colors[color];
};

theme.resetCSS = function(document) {
    vein.setDocument(document);
    vein.inject('body', {
        'background-color': this.color('background'),
        'color': this.color('foreground')
    }).inject('.bar', {
        'background-color': this.color('titlebar'),
        'box-shadow': "0 0 10px 2px " + this.color(3)
    }).inject('input#inputbar', {
        'background-color': this.color('background'),
        'border': "1px solid " + this.color('titlebar'),
        'color': this.color('foreground')
    }).inject('input#inputbar:focus', {
        'box-shadow': "0 0 5px 0 " + this.color('teal'),
        'border-color': this.color('teal')
    }).inject('span.jarvis', {
        'color': this.color('orange')
    }).inject('span.user', {
        'color': this.color('blue')
    }).inject('span.error', {
        'color': this.color('red')
    }).inject('::-webkit-scrollbar-track', {
        'background-color': this.color('titlebar'),
        'border-left': "1px solid " + this.color(5)
    }).inject('::-webkit-scrollbar-thumb', {
        'background-color': this.color(5)
    }).inject('::-webkit-scrollbar-thumb:hover', {
        'background-color': this.color(4)
    });
};

module.exports = theme;