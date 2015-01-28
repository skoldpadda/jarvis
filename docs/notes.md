# Notes

Random notes I've collected while working on jarvis. If there's any link rot here please let me know.

## Versioning

What "jarvis" stands for should change as it evolves. Currently:

Just A

- [ ] Rather
- [x] Really

Very

- [x] Idiotic
- [ ] Immature
- [ ] Imperfect
- [ ] Intelligent
- [ ] Ideal

Shell

## Related Projects

### "AI" Assistants

- [Betty](https://github.com/pickhardt/betty) by `@pickhardt`, an "English-like interface for your command line"
- [howdoi](https://github.com/gleitz/howdoi) by `@gleitz`: "instant coding answers via the command line"
- [Jarvis](https://github.com/cranklin/Jarvis) by `@cranklin`, and related [blog post](http://cranklin.wordpress.com/2012/01/13/building-my-own-siri-jarvis/)
- [E.V.E.](https://github.com/thomasweng15/E.V.E.) by `@thomasweng15`
- [LISA](https://github.com/Seraf/LISA) by `@Seraf`
- [Jarvis](https://github.com/debugger22/Jarvis) by `@debugger22`
- [Home Assistant](https://github.com/balloob/home-assistant) by `@balloob`

### Re-imagining the Shell

- [TermKit](https://github.com/unconed/TermKit) by `@unconed`
- [shotgun](https://github.com/chevex/shotgun) by `@chevex`
- [nshell](https://github.com/visionmedia/nshell) by `@visionmedia`
- [Cloud Commander](https://github.com/coderaiser/cloudcmd) by `@coderaiser`
- [Pigshell](https://github.com/pigshell/pigshell) by `@pigshell`
- [GCLI](https://github.com/joewalker/gcli) by `@joewalker` and the [site](http://mozilla.github.io/gcli/)
- [Rich Command Shells](http://waywardmonkeys.org/2014/10/10/rich-command-shells/) article

### The Internet of Things

- [wit.ai](https://wit.ai/)
- [Node-RED](https://github.com/node-red/node-red) by `@node-red`

## Languages

### Erlang/Elixir

- [This](http://blog.glaucocustodio.com/2014/08/12/setting-up-an-elixir-erlang-development-environment-on-ubuntu/) helps you get all set on Ubuntu
- [n2o](https://github.com/5HT/n2o) is an Erlang Websocket-powered server: see [slides about it](http://kukuruku.co/hub/erlang/n2o-erlang-web-framework) and its [use in Elixir](https://github.com/erlang-synrc/n2o.elixir)
- See [Rise of the Phoenix](https://github.com/erlang-synrc/n2o.elixir) slides, especially the part about Phoenix Services
- [Python for distributed Erlang](https://github.com/lfex/py)
- [**Huge list of Erlang bookmarks**](https://github.com/0xAX/erlang-bookmarks/blob/master/ErlangBookmarks.md)
- [Erlang for embedded devices](http://nerves-project.org/)

### JavaScript

- [Keypress](http://dmauro.github.io/Keypress/), a library for advanced keypress detection
- [NeDB](https://github.com/louischatriot/nedb), an "embedded persistent database for node.js"

### Node

- [shoe-bin](https://github.com/substack/shoe-bin) is a wrapper of SockJS for use with streams
- Use [node-trumpet](https://github.com/substack/node-trumpet) or [hyperstream](https://github.com/substack/hyperstream) to stream updates to the DOM
- [Synaptic](http://synaptic.juancazala.com/) neural networks for Node

### Python

- [Messaging in IPython](http://ipython.org/ipython-doc/stable/development/messaging.html), which uses ZeroMQ so is more useful just for the specs
- PyMOTW multiprocessing [Basics](http://pymotw.com/2/multiprocessing/basics.html) and [Queues](http://pymotw.com/2/multiprocessing/communication.html#multiprocessing-queues)
- Interesting [SO question](http://stackoverflow.com/questions/4995419/in-python-how-do-i-know-when-a-process-is-finished) about process cleanup
- [Blog post](http://honnibal.wordpress.com/2013/12/18/a-simple-fast-algorithm-for-natural-language-dependency-parsing/) about parsing English with 500 lines of Python

## Miscellaneous

### Knowledge

- For computational knowledge, use TheBigDB in the style of [Akiva](https://github.com/thebigdb/akiva)
- Jeannie is an existing voice assistant with a great [REST API](https://www.mashape.com/pannous/jeannie) and related [GitHub project](https://github.com/pannous/jeannie-webclient)
- [NLUlite](https://nlulite.com/) "natural language parser and database"

### HTML5 Applications

- Two great posts by Clint Berry, [one](http://clintberry.com/2013/html5-apps-desktop-2013/) about the various framework options, [another](http://clintberry.com/2013/html5-desktop-apps-with-brackets-shell/) about using the Brackets Shell
- [Shadow DOM](http://www.html5rocks.com/en/tutorials/webcomponents/shadowdom/) to separate module CSS/JS as in [Atom](http://blog.atom.io/2014/11/18/avoiding-style-pollution-with-the-shadow-dom.html)

### UI Design

- JSON-backed form structures
    - A giant list of possible options in a [SO question](http://stackoverflow.com/questions/998832/gui-based-or-web-based-json-editor-that-works-like-property-explorer)
    - [Alpaca](http://www.alpacajs.org/examples/forms/customer-profile/edit-form.html), which defines a schema to render the form
    - A full-on [JSON editor](https://github.com/DavidDurman/FlexiJsonEditor), not quite necessary for form manipulation
    - [jquery.dform](https://github.com/daffl/jquery.dform), heavyweight library for full JSON backing
    - **Best one**: [JSON Editor](https://github.com/jdorn/json-editor) by `@jdorn`
- [UI Gradients](http://uigradients.com/) provided the color schemes for the Orpheus, Apollo, and Charon logos
- [This](http://zachholman.com/images/posts/chat.png) is what the chat should look like

### Streams, etc.

- [Stream Handbook](https://github.com/substack/stream-handbook)
- [Communicating Sequential Processes](http://en.wikipedia.org/wiki/Communicating_sequential_processes) (CSP)
    - Clojure data streaming philosophy (core.async)
    - There's a nice blog post about [CSP in JavaScript](http://jlongster.com/Taming-the-Asynchronous-Beast-with-CSP-in-JavaScript), and the [js-csp GitHub repo](https://github.com/ubolonton/js-csp)
    - [mori](http://swannodette.github.io/mori/) allows for persistent data structures in JS, since immutable data resolves a lot of issues with application state
    - Another [JS CSP implementation](http://sriku.org/blog/2014/02/11/bye-bye-js-promises/)
- Functional Reactive Programming (FRP)
    - See the [Reactive Manifesto](http://www.reactivemanifesto.org/)
    - [Introduction to Reactive Programming](https://gist.github.com/staltz/868e7e9bc2a7b8c1f754/) article
    - [RxJS](https://github.com/Reactive-Extensions/RxJS) is an implementation of this philosophy
    - Elm is a concurrent FRP language, see [this thing](https://gist.github.com/evancz/2b2ba366cae1887fe621) on Elm's architecture
    - [This dissertation](http://www.cs.cornell.edu/~jnfoster/papers/jnfoster-dissertation.pdf) on "bidirectional programming" may be of use if it wasn't so dissertation-ey
    - React is a loose implementation of FRP, and [Om](http://josf.info/blog/2014/09/18/first-ompressions-a-conceptual-look-at-om/) is Clojure + React
- We can use CSP and FRP [together](http://stackoverflow.com/questions/20632512/comparing-core-async-and-functional-reactive-programming-rx): CSP separates concerns over processes (the "message passing"), while FRP handles propagating data once the underlying model changes
- [Operational Transformation](http://en.wikipedia.org/wiki/Operational_transformation) for concurrent apps
    - See [ShareJS](http://sharejs.org/) and [Derby](http://derbyjs.com/)
- [Flow-based Programming](http://www.jpaulmorrison.com/fbp/)
    - Leads to [NoFlo](http://noflojs.org/) and [Flowhub](https://flowhub.io/)

### Worker Sandboxing

- [jailed](https://github.com/asvd/jailed) provides a model for isolating spawned subprocesses with restricted privileges
- You can proxy arbitrary code in some language to this [code runner](http://colabv6.dan.co.jp/lleval.html), see the Hubot script [eval.coffee](https://github.com/github/hubot-scripts/blob/master/src/scripts/eval.coffee) for an example usage
- [Polyglot](https://github.com/sausheong/polyglot) has a model that allows for writing a worker in any language
- See [neovim's plugin architecture](https://github.com/neovim/neovim/wiki/Plugin-UI-architecture) for a sense of how UI can be propagated to a client (neovim itself is headless)

### Unix

- [A guide](http://monkey.org/~marius/unix-tools-hints.html) on how to write UNIX tools

### Ideas

- Chris Granger on [the IDE as data](http://www.chris-granger.com/2013/01/24/the-ide-as-data/)
- Bret Victor on [learnable programming](http://worrydream.com/#!/LearnableProgramming)
- Martin Fowler on [microservices](http://martinfowler.com/articles/microservices.html)

## Thoughts

- msgpack vs. JSON?
- Docker?
