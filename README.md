![jarvis](https://raw.github.com/willyg302/jarvis/master/media/jarvis-logo.png "Sometimes you have to run before you can walk")

---

**Just A Really Very Idiotic Shell** -- version 0.1.0

jarvis is for me, not you (at least at the moment). If you have somehow stumbled upon this repo, hurry along and pay it no heed.

...Still want to run it? Okay. Don't say I didn't warn you.

## Setup

> **Note**: On Windows, use the PowerShell instead of CMD.exe! On Linux you may have to do a [symlink](https://github.com/rogerwang/node-webkit/wiki/The-solution-of-lacking-libudev.so.0).

1. Install [Node.js and NPM](http://nodejs.org/) -- ensure that these are in your path!

2. Make sure Git is installed on your system (`git --version`, for Windows [this](http://git-scm.com/) is a good solution)

3. Get [Python](http://www.python.org/) (we use 2.7)

4. Install [strap.py](https://github.com/willyg302/strap.py)

5. Grab jarvis!

   ```
   strap init gh:willyg302/jarvis -d jarvis
   ```

### Running

Made it this far? Awesome. Now run that bad boy.

```bash
cd jarvis
strap
```

At this point you can visit `localhost:8080` to see an in-browser reference implementation of the jarvis frontend. If you want to run the standalone node-webkit based frontend, just do `npm run app` after starting the kernel.

### Building

> **Note**: Currently only builds the node-webkit GUI. Eventually, the kernel should be packaged along with the app (somehow).

```
npm run deploy
```

The final application builds of jarvis will be located in `dist/` for each major operating system.

## Spec

For more about the project's goals and design, see the [spec](docs/spec.md).

## Todo

Besides everything marked [`@TODO`](https://github.com/willyg302/jarvis/search?q=%22%40TODO%22) in any source file.

- [ ] "clip.py" -- better CLI parser, perhaps a mix of docopt and click
- [ ] Data persistence via rudimentary "brain", a la Hubot
- [ ] Provide methods for running built-in shell commands, possibly via [shell.js](https://github.com/arturadib/shelljs)
- [ ] Settings file (akin to bash profiles) -- also manageable through Control Panel?
- [ ] Establish reliable, extensible kernel/client protocol
- [ ] Control Panel (settings, theme management, etc.)