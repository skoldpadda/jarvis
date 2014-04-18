import shlex

from tornado.template import Template


'''
@TODO:
  - Have a method that allows scripts to send messages arbitrarily (print --> broadcast)
'''

# Adapted from: http://www.valuedlessons.com/2008/04/events-in-python.html
class Event:

	def __init__(self):
		self.handlers = set()

	def handle(self, handler):
		self.handlers.add(handler)
		return self

	def unhandle(self, handler):
		self.handlers.discard(handler)
		return self

	def fire(self, *args, **kwargs):
		for handler in self.handlers:
			handler(*args, **kwargs)

	def get_handler_count(self):
		return len(self.handlers)

	__iadd__ = handle
	__isub__ = unhandle
	__call__ = fire
	__len__  = get_handler_count



# https://github.com/willyg302/jarvis/blob/3e254dde64587b58c5fe9c8bcd335815dd3221b5/jarvis.py




# @TODO: Error-checking! Does directory exist? spaces in directory name? if user just types "cd", go back to home!
def cd(args):
	return 'cd'

def help(args):
	return 'help'

def history(args):
	return 'history'


# A dictionary of commands in this file
builtins = {
	'cd': cd,
	'help': help,
	'history': history,
}




'''
Kernel.prototype.userInput = function(input) {
	var self = this;

	// @TODO: should it really be printed out in all cases?
	self.userMessage(input);

	if (!input) {
		return;
	}

	/**
	 * 1. Is it a built-in function? (right in this class)
	 * 2. Is it a script in plugins/ folder (recursive)?
	 * 3. Is it a native shell command?
	 * 4. Pass to semantic analyzer
	 */

	// @TODO: This is horrible hack
	var parsed = input.match(/(?:[^\s"]+|"[^"]*")+/g);
	var cmd = parsed[0];
	var args = parsed.slice(1);

	// Close?
	if (['exit', 'quit', 'bye'].indexOf(cmd) > -1) {
		self.emit('trigger_close');
		return;
	}


	// Where cmd is a string
	if (cmd in builtins && typeof builtins[cmd] === "function") {
		self.emit('kernel_out', builtins[cmd](args));
		return;
	}

	// @TODO: Consider, is try-catching errant input too expensive?
	try {
		var script = utils.userRequire("scripts/" + cmd);
		var out = script.run(args);
		if (out) {
			self.emit('kernel_out', out);
		}
		return;
	} catch (err) {
		//console.log(err);
	}


	// @TODO: This is great for debugging, but it should be copied over...(into jarvis-data/)
	try {
		var script = require("../user/scripts/" + cmd);
		var out = script.run(args);
		if (out) {
			self.emit('kernel_out', out);
		}
		return;
	} catch (err) {
		console.log(err);
	}


	/** So it turns out fork() is broken in node-webkit. This is a bummer. https://github.com/rogerwang/node-webkit/issues/213
	 * Not that we'd really NEED async second-process execution though? I mean it's cleaner...
	 * but in the Jarvis model in -> out makes just as much sense.
	 * Possible workaround: https://gist.github.com/iamkvein/2006752
	 * Basically, we implement our own common abstraction, or perhaps intercept process.stdout/stderr.
	var child = cp.fork("./plugins/" + cmd);
	child.stdout.on('data', function(data) {
		console.log('stdout: ' + data);
	});
	child.send(args);
	*/


	self.emit('kernel_err', "Unrecognized command \"" + cmd + "\"");

	return self;
};
'''



'''

 def user_enter(self, uin):
		self.user_message(uin)
		if uin:
			# @TODO: This should not happen here. If for example the user types "i'm doing fine" (note the quote)
			# shlex will throw a ValueError
			raw_cmd = shlex.split(uin)
			if raw_cmd[0] in ['exit', 'quit', 'bye']:
				QCoreApplication.instance().quit()
			else:
				runCommand(raw_cmd[0], raw_cmd[1:])
'''



'''
kernel.on('kernel_out', function(data) {
	printMessage({"text": data + "\n"});
});

kernel.on('kernel_err', function(data) {
	printMessage({"text": "<span style=\"color:" + theme_manager.color('red') + ";\">" + data + "</span>\n"});
});

kernel.on('trigger_close', function() {
	close();
});


Kernel.prototype.jarvisMessage = function(message) {
	this.emit('message', {"author": "jarvis", "tag": JARVIS.NAME + " > ", "text": message + "\n"});
};

'''

'''
/*

Kernel.prototype.postInit = function() {
	this.jarvisMessage("Starting up on " + moment().format('MMMM Do YYYY, h:mm:ss a'));
};


Kernel.prototype.jarvisMessage = function(message) {
	this.emit('message', {"author": "jarvis", "tag": JARVIS.NAME + " > ", "text": message + "\n"});
};


*/
'''

class Kernel:

	def __init__(self):
		self.direct_channel = Event()  # Call with: self.direct_channel({SOME JSON HERE})

	def runCommand(self, command, args):
		c = self.__class__
		if hasattr(c, command) and callable(getattr(c, command)):
			return getattr(c, command)(self, args)
		return Command.list(command)  # Unrecognized command, show list of known commands

	# Takes a JSON input, returns a JSON output. Returns empty dict if doesn't want to handle stuff
	def handle_input(self, message):
		# log.info('Servicing request: {}'.format(string))
		# raw_cmd = shlex.split(string)
		# return self.runCommand(raw_cmd[0], raw_cmd[1:])
		if not message['text']:
			return {}

		return {'text': message['text']}