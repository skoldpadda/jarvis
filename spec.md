# Design Specification

## Goals

**Note**: This section is a work-in-progress.

### A "Semantic" Shell

> It is not our duty to understand the arbitrary, meaningless dictates of machines.

> -- Don Norman, *The Design of Everyday Things*

For me, the shell -- whether it be cmd or bash -- is an "everyday thing". You'd think that after all this time I'd be completely comfortable with using a shell, but I'm not. There's not a day that goes by that I don't forget what script does what, or confuse which flag combinations to use, or make a typo and screw something up.

The shell is not forgiving.

Of course, it's not entirely the shell's fault. It just does what we tell it to. But therein lies the problem: humans are altogether incredibly faulty creatures. Pair that with a dumb terminal and you have a recipe for disaster.

I want a shell that understands. I want a shell that asks me, "Why are you trying to `rm -r /`?" before I wreck my laptop. This is not an impossible goal; I can already whip out my phone and talk to an artificial assistant in a natural language about stock prices, the weather, and what meetings I have scheduled in the afternoon. Why these facilities are not also on my desktop is beyond me.

### Smart Data Display

> Evolve output beyond the monospace character grid; use rich media and design.

> -- Steven Wittens, *TermKit*

It should come as no surprise that TermKit is one of the inspirations for jarvis. The idea that a shell should be able to display syntax-highlighted code or play videos is a compelling one.

However, upon looking at TermKit's code I was slightly disappointed. A lot of the formatting for this "rich media" was handled by hard-coded CSS. In reality, the data itself should dictate how it's displayed in a uniform and predictable way.

### What jarvis Won't Be

- **A complete bash replacement**

  For all its shortcomings, bash has stood the test of time because it does what it does remarkably well. jarvis is not intended to be its replacement, but rather a supplement focusing on the above goals. As such, things like full-screen buffers (e.g. vi, emacs) and bash scripting will not be supported.

## Architecture

@TODO

## Communication Protocol

@TODO

## Script System

@TODO

## Control Panel

Clicking the jarvis icon to the left of the omnibar opens the Control Panel.

@TODO

## Interaction Scenarios

- Asynchronous task completion (possibly handled by the Control Panel)
- Drag/drop of files and data to/from the shell

## References

### Related Work

- [TermKit](https://github.com/unconed/TermKit)
- [Shotgun](https://github.com/chevex/shotgun)
- [nshell](https://www.npmjs.org/package/nshell)
