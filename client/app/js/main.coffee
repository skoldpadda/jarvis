riot = require 'riot'
require './chat.tag'


chatObserver = riot.observable()
riot.mount 'chat', chatObserver


chat = document.getElementById 'jarvis-chat'
jarvisInput = document.getElementById 'jarvis-input'
socket = new Phoenix.Socket '/kernel'
clientChannel = null




socket.connect()

socket.join('client:echo', {}).receive 'ok', (channel) ->
	channel.on 'return_event', (message) ->
		jarvisMessage message.data

	channel.on 'join', (message) ->
		console.log message.data

	clientChannel = channel

sendToKernel = (message) ->
	if not clientChannel?
		return
	clientChannel.push 'echo', { data: message }


# MESSAGING

printMessage = (author, message) ->
	chatObserver.trigger 'message', {
		author: author,
		message: message
	}
	chat.parentNode.scrollTop = chat.parentNode.scrollHeight

userMessage = (message) ->
	printMessage 'User', message
	sendToKernel message

appMessage = (message) ->
	printMessage 'App', message

jarvisMessage = (message) ->
	printMessage 'jarvis', message


onInputBarKeypress = (e) ->
	e ?= window.event
	# Enter pressed?
	if e.keyCode is 10 or e.keyCode is 13
		userInput = jarvisInput.value
		jarvisInput.value = ''
		userMessage userInput


# INITIALIZATION

window.onload = ->
	jarvisInput.onkeypress = onInputBarKeypress
	jarvisInput.focus()
