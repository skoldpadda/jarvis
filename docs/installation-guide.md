# Installation Guide

This guide will help you get up and running with jarvis. The installation process has been automated as much as possible via strap, but may not work on all platforms. If you run into problems with the automated installation, follow the manual installation instructions instead.

## Prerequisites

- [Python 2.7.x](http://www.python.org/)
- [strap](https://github.com/willyg302/strap.py)

## Installing Manually (The Hard Way)

In addition to the above prerequisites, you will need the following:

- [Node.js and NPM](http://nodejs.org/)
- [Erlang/OTP 17.1](http://www.erlang.org/download_release/25)
- [Elixir v1.0.0](http://elixir-lang.org/install.html)
- [Phoenix v0.4.1](https://github.com/phoenixframework/phoenix)

```bash
git clone git@github.com:willyg302/jarvis.git
cd jarvis
strap run post_install
```

## Using strap (The Easy Way)

```bash
strap init gh:willyg302/jarvis -d jarvis
```

If you run into any issues along the way, follow the on-screen instructions to troubleshoot.
