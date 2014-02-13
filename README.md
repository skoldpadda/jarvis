# jarvis

Just A Really Very Idiotic Shell - version 0.1.0

jarvis is for me, not you (at least at the moment). If you have somehow stumbled upon this repo, hurry along and pay it no heed.

...Still want to run it? Okay. Don't say I didn't warn you.

## Setup

> **Note**: On Windows, use the PowerShell instead of CMD.exe! On Linux you may have to do a [symlink](https://github.com/rogerwang/node-webkit/wiki/The-solution-of-lacking-libudev.so.0).

1. Install [Node.js and NPM](http://nodejs.org/) -- ensure that these are in your path!

2. Make sure Git is installed on your system (`git --version`, for Windows [this](http://git-scm.com/) is a good solution)

3. Install [init-skeleton](https://github.com/paulmillr/init-skeleton): `npm install -g init-skeleton`

4. Grab jarvis!

   ```
   init-skeleton gh:willyg302/jarvis jarvis
   ```

5. Run that bad boy

   ```
   npm run app
   ```

6. Ready to build?

   ```
   npm run deploy
   ```

   The final application builds of jarvis will be located in `dist/` for each major operating system.

> **Note**: The builds actually currently don't work. But they will. Soon.

## Spec

For more about the project's goals and design, see the [spec](spec.md).

## Todo

Besides everything marked `@TODO` in any source file. **Note**: completed tasks are marked with a ✔.

☐ Provide methods for running built-in shell commands, possibly via [shell.js](https://github.com/arturadib/shelljs)

☐ Settings file (akin to bash profiles) -- also manageable through Control Panel?

☐ Establish reliable, extensible kernel/client protocol

☐ Control Panel (settings, theme management, etc.)