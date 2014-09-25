# jarvis Client

This is a reference implementation of the jarvis client. It is built into Orpheus and served at `/` when jarvis is running.

Because all kernel-client communication is done via sockets, it should be fairly easy to construct clients for other platforms (e.g. using [node-webkit](https://github.com/rogerwang/node-webkit)) or even embed jarvis in a larger system.
