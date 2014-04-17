var JARVIS = window.JARVIS = {
    NAME: 'jarvis',
    VERSION: '0.1.0',
    DEBUG: true,
};


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

function ctrlpanel() {
    // @TODO: This is convenient, but really we need our own control panel
    //JARVIS.win.showDevTools();
}


function refreshTheme() {
    var foreground = '#1d1f21';
    var blue = '#4271ae';

    var but = {
        'up': {'bg': {'color': foreground, 'opacity': '0.0'}, 'fg': {'color': foreground, 'opacity': '0.2'}},
        'over': {'bg': {'color': foreground, 'opacity': '0.0'}, 'fg': {'color': foreground, 'opacity': '1.0'}},
        'down': {'bg': {'color': foreground, 'opacity': '0.0'}, 'fg': {'color': blue, 'opacity': '1.0'}}
    };

    createButton('ctrlpanel', but, ctrlpanel);
}

function resetTitlebarText(text) {
    document.getElementsByClassName('titlebar-text')[0].innerHTML = JARVIS.NAME + " - " + text;
}


/** MESSAGING **/

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
        'author': 'user',
        'tag': 'User',  // @TODO
        'text': message
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


/** INITIALIZATION **/

function initSockJS() {
    appMessage('Connecting to kernel...');
    conn = new SockJS('http://localhost:8080/kernel');
    conn.onopen = function() {
        connOpen = true;
    };
    conn.onmessage = function(e) {
        var data = JSON.parse(e.data);
        printMessage(data);
    };
    conn.onclose = function() {
        conn = null;
        // @TODO ?
    };
}

window.onload = function() {
    refreshTheme();
    resetTitlebarText(JARVIS.NAME);  // @TODO: this
    document.getElementById('inputbar').onkeypress = onInputBarKeypress;
    document.getElementById('inputbar').focus();

    initSockJS();
};