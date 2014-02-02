var gui = require('nw.gui'), win = gui.Window.get();
var os = require('os');

// External libraries
var moment = require('./js/lib/moment.js');

// Our kernel
var Kernel = require('./js/kernel.js');
var myKernel = new Kernel();


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
    win.minimize();
}

function maximize() {
    win.maximize();
}

function restore() {
    win.unmaximize();
}

function close() {
    win.close();
}

function ctrlpanel() {
    // @TODO: This is convenient, but really we need our own control panel
    win.showDevTools();
}


function refreshTheme(theme) {


/*
DEFAULT:

FROM https://github.com/chriskempson/tomorrow-theme/blob/master/Brackets/brackets_theme_tomorrow.less
Note that the tomorrow theme in base16 is modified and not as good

@background: #ffffff;
@current-line: #efefef;
@foreground: #4d4d4c;
@comment: #8e908c;
@red: #c82829;
@orange: #f5871f;
@yellow: #eab700;
@green: #718c00;
@aqua: #3e999f;
@blue: #4271ae;
@purple: #8959a8;


*/
    
    var foreground = "#4d4d4c";
    var blue = "#4271ae";
    var red = "#c82829";
    var titlebar = "#efefef";


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
}


function printMessage(message) {
    var content = document.getElementById("content");
    if (message.hasOwnProperty('tag')) {
        content.innerHTML += "<span class=\"" + message.author + "\">" + message.tag + "</span> ";
    }
    content.innerHTML += message.text.replace('\n', '<br>').replace(' ', '&nbsp;');
    content.parentNode.scrollTop = content.parentNode.scrollHeight;
}

function jarvisMessage(message) {
    printMessage({"author": "jarvis", "tag": "Jarvis > ", "text": message + "\n"});
}

function userMessage(message) {
    printMessage({"author": "user", "tag": os.hostname() + " > ", "text": message + "\n"});
}


function getUserHome() {
    return process.env.HOME || process.env.HOMEPATH || process.env.USERPROFILE;
}

function resetTitlebarText(text) {
    document.getElementsByClassName("titlebar-text")[0].innerHTML = "Jarvis - " + text;
}

function onInputBarKeypress(e) {
    if (typeof e == 'undefined' && window.event) {
        e = window.event;
    }
    // Enter pressed?
    if (e.keyCode == 10 || e.keyCode == 13) {
        user_input = document.getElementById("inputbar").value;
        document.getElementById("inputbar").value = "";
        myKernel.userInput(user_input);
    }
}

myKernel.on('user_input_acknowledged', function(input) {
    userMessage(input);
});


window.onload = function() {
    refreshTheme();

    document.getElementById("inputbar").onkeypress = function(e) {
        onInputBarKeypress(e);
    };

    resetTitlebarText(getUserHome());

    win.show();

    document.getElementById("inputbar").focus();
    jarvisMessage("Starting up on " + moment().format('MMMM Do YYYY, h:mm:ss a'));
}



/** WINDOW EVENTS **/

win.on('close', function() {
    this.hide();  // Pretend to be closed already
    // Do things that need cleaning up
    this.close(true);
});

win.on('maximize', function() {
    document.getElementById("maximize").style.visibility = "hidden";
    document.getElementById("restore").style.visibility = "visible";
});

win.on('unmaximize', function() {
    document.getElementById("restore").style.visibility = "hidden";
    document.getElementById("maximize").style.visibility = "visible";
});