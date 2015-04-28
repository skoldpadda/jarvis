# Installation Guide

This guide will help you get up and running with jarvis. The installation process has been automated as much as possible via ok, but may not work on all platforms. If you run into problems with the automated installation, follow the manual installation instructions instead.

## Prerequisites

- [Python 2.7.x](http://www.python.org/)
- [ok](https://github.com/willyg302/ok)

## Installing Manually (The Hard Way)

In addition to the above prerequisites, you will need the following:

- [Node.js and NPM](http://nodejs.org/)
- [Erlang/OTP 17.5](http://www.erlang.org/download_release/28)
- [Elixir v1.0.4](http://elixir-lang.org/install.html)

```bash
git clone git@github.com:willyg302/jarvis.git
cd jarvis
ok run install
```

## Using ok (The Easy Way)

```bash
ok init gh:willyg302/jarvis
```

If you run into any issues along the way, follow the on-screen instructions to troubleshoot.
