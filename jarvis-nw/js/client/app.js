var JARVIS = window.JARVIS = global.JARVIS = {
    gui: require('nw.gui'),
    win: require('nw.gui').Window.get(),

    NAME: 'jarvis',
    VERSION: '0.1.0',
    DEBUG: true,

    PLATFORM_WINDOWS: process.platform === 'win32',
    PLATFORM_MAC: process.platform === 'darwin',
    PLATFORM_LINUX: process.platform === 'linux'
};


// Our kernel
var Kernel = require('./js/kernel/kernel.js');
var utils = require('./js/kernel/utils.js');
var kernel = new Kernel();

var theme_manager = require('./js/client/theme.js');


/** BUTTONS **/

function styleIcon(icon, theme) {
    var bg = icon.getElementsByClassName("bg")[0];
    bg.setAttribute("fill", theme.bg.color);
    bg.setAttribute("fill-opacity", theme.bg.opacity);

    var fg = icon.getElementsByClassName("fg")[0];
    fg.setAttribute("fill", theme.fg.color);
    fg.setAttribute("fill-opacity", theme.fg.opacity);
}

function createButton(name, theme, func) {
    var svgobj = document.getElementById(name),
        svg = svgobj.contentDocument,
        svgclick = svg.getElementsByClassName("click")[0];

    styleIcon(svg, theme.up);

    svgclick.onmouseover = function() {
        styleIcon(svg, theme.over);
    };
    svgclick.onmouseout = function() {
        styleIcon(svg, theme.up);
    };
    svgclick.onmousedown = function() {
        styleIcon(svg, theme.down);
    };
    svgclick.onmouseup = function() {
        styleIcon(svg, theme.over);
    };
    svgclick.onclick = function() {
        func();
    };
}

function minimize() {
    JARVIS.win.minimize();
}

function maximize() {
    JARVIS.win.maximize();
}

function restore() {
    JARVIS.win.unmaximize();
}

function close() {
    JARVIS.win.close();
}

function ctrlpanel() {
    // @TODO: This is convenient, but really we need our own control panel
    //JARVIS.win.showDevTools();
}


function refreshTheme(name) {
    theme_manager.loadTheme(name);

    var foreground = theme_manager.color('foreground');
    var blue = theme_manager.color('blue');
    var red = theme_manager.color('red');
    var titlebar = theme_manager.color('titlebar');

    var but1 = {
        "up": {"bg": {"color": foreground, "opacity": "0.0"}, "fg": {"color": foreground, "opacity": "0.2"}},
        "over": {"bg": {"color": foreground, "opacity": "0.08"}, "fg": {"color": foreground, "opacity": "1.0"}},
        "down": {"bg": {"color": blue, "opacity": "1.0"}, "fg": {"color": titlebar, "opacity": "1.0"}}
    };
    var but2 = {
        "up": {"bg": {"color": foreground, "opacity": "0.0"}, "fg": {"color": foreground, "opacity": "0.2"}},
        "over": {"bg": {"color": red, "opacity": "1.0"}, "fg": {"color": titlebar, "opacity": "1.0"}},
        "down": {"bg": {"color": foreground, "opacity": "1.0"}, "fg": {"color": titlebar, "opacity": "1.0"}}
    };
    var but3 = {
        "up": {"bg": {"color": foreground, "opacity": "0.0"}, "fg": {"color": foreground, "opacity": "0.2"}},
        "over": {"bg": {"color": foreground, "opacity": "0.0"}, "fg": {"color": foreground, "opacity": "1.0"}},
        "down": {"bg": {"color": foreground, "opacity": "0.0"}, "fg": {"color": blue, "opacity": "1.0"}}
    };

    createButton("minimize", but1, minimize);
    createButton("maximize", but1, maximize);
    createButton("restore", but1, restore);
    createButton("close", but2, close);
    createButton("ctrlpanel", but3, ctrlpanel);

    // Now we reset CSS
    theme_manager.resetCSS(document);

}

function printMessage(message) {
    var content = document.getElementById("content");
    if (message.hasOwnProperty('tag')) {
        content.innerHTML += "<span class=\"" + message.author + "\">" + message.tag + "</span>";
    }
    content.innerHTML += message.text;
    content.parentNode.scrollTop = content.parentNode.scrollHeight;
}

function resetTitlebarText(text) {
    document.getElementsByClassName("titlebar-text")[0].innerHTML = JARVIS.NAME + " - " + text;
}

function onInputBarKeypress(e) {
    if (typeof e == 'undefined' && window.event) {
        e = window.event;
    }
    // Enter pressed?
    if (e.keyCode == 10 || e.keyCode == 13) {
        user_input = document.getElementById("inputbar").value;
        document.getElementById("inputbar").value = "";
        kernel.userInput(user_input);
    }
}

kernel.on('message', function(data) {
    printMessage(data);
});

kernel.on('kernel_out', function(data) {
    printMessage({"text": data + "\n"});
});

kernel.on('kernel_err', function(data) {
    printMessage({"text": "<span style=\"color:" + theme_manager.color('red') + ";\">" + data + "</span>\n"});
});

kernel.on('trigger_close', function() {
    close();
});


window.onload = function() {
    // Start our kernel @TODO: asynchronously?
    kernel.boot();

    var settings = utils.userRequire('settings.js');  // @NOTE: Cannot userRequire() until AFTER booting kernel!
    refreshTheme(settings.theme);
    resetTitlebarText(utils.getUserHome());

    document.getElementById("inputbar").onkeypress = function(e) {
        onInputBarKeypress(e);
    };
    JARVIS.win.show();
    document.getElementById("inputbar").focus();
    kernel.postInit();
}

window.addEventListener('keydown', function(e) {
    if (e.keyIdentifier === 'F12') {
        JARVIS.win.showDevTools();
    }
});


/** WINDOW EVENTS **/

JARVIS.win.on('close', function() {
    this.hide();  // Pretend to be closed already
    // Do things that need cleaning up
    this.close(true);
});

JARVIS.win.on('maximize', function() {
    document.getElementById("maximize").style.visibility = "hidden";
    document.getElementById("restore").style.visibility = "visible";
});

JARVIS.win.on('unmaximize', function() {
    document.getElementById("restore").style.visibility = "hidden";
    document.getElementById("maximize").style.visibility = "visible";
});