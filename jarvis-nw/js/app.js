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

var fs = require('fs-extra'),
    path = require('path');

var utils = require('./js/utils.js'),
    theme_manager = require('./js/theme.js');

var conn = null;
var connOpen = false;


/** BUTTONS **/

function styleIcon(icon, theme) {
    var bg = icon.getElementsByClassName('bg')[0];
    bg.setAttribute('fill', theme.bg.color);
    bg.setAttribute('fill-opacity', theme.bg.opacity);

    var fg = icon.getElementsByClassName('fg')[0];
    fg.setAttribute('fill', theme.fg.color);
    fg.setAttribute('fill-opacity', theme.fg.opacity);
}

function createButton(name, theme, func) {
    var svgobj = document.getElementById(name),
        svg = svgobj.contentDocument,
        svgclick = svg.getElementsByClassName('click')[0];

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
        'up': {'bg': {'color': foreground, 'opacity': '0.0'}, 'fg': {'color': foreground, 'opacity': '0.2'}},
        'over': {'bg': {'color': foreground, 'opacity': '0.08'}, 'fg': {'color': foreground, 'opacity': '1.0'}},
        'down': {'bg': {'color': blue, 'opacity': '1.0'}, 'fg': {'color': titlebar, 'opacity': '1.0'}}
    };
    var but2 = {
        'up': {'bg': {'color': foreground, 'opacity': '0.0'}, 'fg': {'color': foreground, 'opacity': '0.2'}},
        'over': {'bg': {'color': red, 'opacity': '1.0'}, 'fg': {'color': titlebar, 'opacity': '1.0'}},
        'down': {'bg': {'color': foreground, 'opacity': '1.0'}, 'fg': {'color': titlebar, 'opacity': '1.0'}}
    };
    var but3 = {
        'up': {'bg': {'color': foreground, 'opacity': '0.0'}, 'fg': {'color': foreground, 'opacity': '0.2'}},
        'over': {'bg': {'color': foreground, 'opacity': '0.0'}, 'fg': {'color': foreground, 'opacity': '1.0'}},
        'down': {'bg': {'color': foreground, 'opacity': '0.0'}, 'fg': {'color': blue, 'opacity': '1.0'}}
    };

    createButton('minimize', but1, minimize);
    createButton('maximize', but1, maximize);
    createButton('restore', but1, restore);
    createButton('close', but2, close);
    createButton('ctrlpanel', but3, ctrlpanel);

    // Now we reset CSS
    theme_manager.resetCSS(document);
}


/** MESSAGING **/

var entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': '&quot;',
    "'": '&#39;',
    "/": '&#x2F;'
};

function escapeHtml(string) {
    return String(string).replace(/[&<>"'\/]/g, function (s) {
        return entityMap[s];
    });
}

function printMessage(message) {
    var content = document.getElementById('content');
    if (message.hasOwnProperty('tag')) {
        content.innerHTML += "<span class=\"" + message.author + "\">" + message.tag + " &gt; </span>";
    }
    content.innerHTML += (message.text + "\n");  // @TODO: Need newline here?
    content.parentNode.scrollTop = content.parentNode.scrollHeight;
}

function sendToKernel(obj) {
    if (!connOpen) {
        return;
    }
    conn.send(JSON.stringify(obj));
}

function userMessage(message) {
    sendToKernel({
        'header': {
            'type': 'input_request'
        },
        'content': {
            'text': message
        }
    });
}

function appMessage(message) {
    printMessage({
        'author': 'app',
        'tag': 'App',
        'text': message
    });
}


function onInputBarKeypress(e) {
    if (typeof e === 'undefined' && window.event) {
        e = window.event;
    }
    // Enter pressed?
    if (e.keyCode === 10 || e.keyCode === 13) {
        user_input = document.getElementById('inputbar').value;
        document.getElementById('inputbar').value = '';
        userMessage(user_input);
    }
}


/** MESSAGE HANDLERS **/

var messageHandlers = {
    input_request: function(data) {
        printMessage({
            'author': 'user',
            'tag': data.header.username,
            'text': escapeHtml(data.content.text)
        });
    },
    input_response: function(data) {
        console.log(data);
        // @TODO: We actually shouldn't escape EVERYTHING.
        // For example, suppose the response is a url with metadata saying it should be inserted as an img
        // Or embedded video? What then?
        var text = escapeHtml(data.content.text);
        if (data.content.err !== undefined) {
            text = '<span class="error">' + text + '</span>';
        }
        printMessage({
            'text': text
        });
    },
    jarvis_message: function(data) {
        printMessage({
            'author': 'jarvis',
            'tag': JARVIS.NAME,  // @TODO: Kernel-side
            'text': escapeHtml(data.content.text)
        });
    },
    handshake_response: function(data) {
        // @TODO: Really the USERNAME should also go in the titlebar so clients know who they are
        // USERNAME = data.header.username;
    },
    property_update: function(data) {
        if (data.content.property === 'current_directory' || data.content.property === 'username') {
            document.getElementById(data.content.property).innerHTML = data.content.value;
        }
    }
};

function handleKernelMessage(data) {
    messageHandlers[data.header.type](data);
}


/** INITIALIZATION **/

// Load settings and user folder, if it doesn't exist make it.
function checkSettings() {
    var u = path.resolve(utils.getUserHome(), 'jarvis-data');
    if (!fs.existsSync(u)) {
        fs.copySync('./js/user', u);
    }
}

function initSockJS() {
    appMessage('Connecting to kernel...');
    conn = new SockJS('http://localhost:8080/kernel');
    conn.onopen = function() {
        connOpen = true;
        sendToKernel({
            'header': {
                'type': 'handshake_request'
            }
        });
    };
    conn.onmessage = function(e) {
        var data = JSON.parse(e.data);
        handleKernelMessage(data);
    };
    conn.onclose = function() {
        conn = null;
        // @TODO ?
    };
}

window.onload = function() {
    checkSettings();
    var settings = utils.userRequire('settings.js');  // @NOTE: Cannot userRequire() until AFTER checkSettings()!
    refreshTheme(settings.theme);
    document.getElementsByClassName('titlebar-text')[0].innerHTML = '<span id="username"></span> - <span id="current_directory"></span>';
    document.getElementById('inputbar').onkeypress = onInputBarKeypress;
    JARVIS.win.show();
    document.getElementById('inputbar').focus();

    initSockJS();
};

window.addEventListener('keydown', function(e) {
    if (e.keyIdentifier === 'F12') {
        JARVIS.win.showDevTools();
    }
});


/** WINDOW EVENTS **/

JARVIS.win.on('close', function() {
    this.hide();  // Pretend to be closed already
    // Do things that need cleaning up
    if (connOpen) {
        conn.close();
        conn = null;
    }
    this.close(true);
});

JARVIS.win.on('maximize', function() {
    document.getElementById('maximize').style.visibility = 'hidden';
    document.getElementById('restore').style.visibility = 'visible';
});

JARVIS.win.on('unmaximize', function() {
    document.getElementById('restore').style.visibility = 'hidden';
    document.getElementById('maximize').style.visibility = 'visible';
});