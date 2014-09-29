var chat = document.getElementById('jarvis-chat');
var jarvisInput = document.getElementById('jarvis-input');
var socket = new Phoenix.Socket('/kernel');
var clientChannel = null;

socket.join('client', 'echo', {}, function(channel) {
	channel.on('return_event', function(message) {
		jarvisMessage(message.data);
	});

	channel.on('join', function(message) {
		console.log(message);
	});

	clientChannel = channel;
});

function sendToKernel(message) {
	if (clientChannel === null) {
		return;
	}
	clientChannel.send('echo', {data: message});
}


/** MESSAGING **/

function printMessage(author, message) {
	if (author !== null) {
		chat.innerHTML += '<span class="' + author.toLowerCase() + '">' + author + ' &gt; </span>';
	}
	chat.innerHTML += (message + "\n");
	chat.parentNode.scrollTop = chat.parentNode.scrollHeight;
}


function userMessage(message) {
	printMessage('User', message);
	sendToKernel(message);
}

function appMessage(message) {
	printMessage('App', message);
}

function jarvisMessage(message) {
	printMessage('jarvis', message);
}


function onInputBarKeypress(e) {
	if (typeof e === 'undefined' && window.event) {
		e = window.event;
	}
	// Enter pressed?
	if (e.keyCode === 10 || e.keyCode === 13) {
		userInput = jarvisInput.value;
		jarvisInput.value = '';
		userMessage(userInput);
	}
}


/** INITIALIZATION **/



window.onload = function() {
	jarvisInput.onkeypress = onInputBarKeypress;
	jarvisInput.focus();
};
