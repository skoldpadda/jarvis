# jarvis

Just A Really Very Idiotic Shell - version 0.1.0

jarvis is for me, not you (at least at the moment). If you have somehow stumbled upon this repo, hurry along and pay it no heed.

...Still want to run it? Okay. You will need the latest [node-webkit](https://github.com/rogerwang/node-webkit#downloads) installed. Then just do `nw jarvis-nw`.

## Workflow

> **Note**: On Windows, use the PowerShell instead of CMD.exe! On Linux you may have to do a [symlink](https://github.com/rogerwang/node-webkit/wiki/The-solution-of-lacking-libudev.so.0).

### Prerequisites

- [Node.js and NPM](http://nodejs.org/)
- Git
- [init-skeleton](https://github.com/paulmillr/init-skeleton): `npm install -g init-skeleton`

### Grab jarvis!

```
init-skeleton gh:willyg302/jarvis jarvis
```

### Run That Bad Boy

```
npm run app
```

### Deploy

```
npm run deploy
```

The final application builds of jarvis will be located in `/dist` for each major operating system.

## Spec

For more about the project's goals and design, see the [spec](spec.md).

## Todo

Besides everything marked `@TODO` in any source file. **Note**: completed tasks are marked with a ✔.

☐ Provide methods for running built-in shell commands, possibly via [shell.js](https://github.com/arturadib/shelljs)

☐ Settings file (akin to bash profiles) -- also manageable through Control Panel?

☐ Establish reliable, extensible kernel/client protocol

☐ Control Panel (settings, theme management, etc.)