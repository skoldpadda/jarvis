var shoe = require('shoe-bin');
var through = require('through2');


var JARVIS = window.JARVIS = {
	NAME: 'jarvis',
	VERSION: '0.1.0',
	DEBUG: true,
};

var conn = null;


function ctrlpanel() {
	console.log('Clicked Control Panel!');
}


/** MESSAGING **/

// @TODO this is terrible
function printMessage(message) {
	var content = document.getElementById('content');
	if (message.hasOwnProperty('tag')) {
		content.innerHTML += '<span class="' + message.author + '">' + message.tag + ' &gt; </span>';
	}
	content.innerHTML += (message.text + "\n");  // @TODO: Need newline here?
	content.parentNode.scrollTop = content.parentNode.scrollHeight;
}

function userMessage(message) {
	printMessage({
		'author': 'user',
		'tag': 'User',
		'text': message
	});
	conn.write(message);
}

function appMessage(message) {
	printMessage({
		'author': 'app',
		'tag': 'App',
		'text': message
	});
}

function jarvisMessage(message) {
	printMessage({
		'author': 'jarvis',
		'tag': JARVIS.NAME,
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
	conn = shoe('/kernel', function() {
		jarvisMessage('Connected!');
	});
	conn.pipe(through(function(message, enc, next) {
		printMessage({'text': message});
		next();
	}));
}

window.onload = function() {
	document.querySelector('#btn-ctrlpanel .click').onclick = function() {
		ctrlpanel();
	}
	document.getElementById('inputbar').onkeypress = onInputBarKeypress;
	document.getElementById('inputbar').focus();

	initSockJS();
};
