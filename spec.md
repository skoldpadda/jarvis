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

### What jarvis Won't Be

- **A complete bash replacement**

  For all its shortcomings, bash has stood the test of time because it does what it does remarkably well. jarvis is not intended to be its replacement, but rather a supplement focusing on the above goals. As such, things like full-screen buffers (e.g. vi, emacs) and bash scripting will not be supported.

## Communication Policy

@TODO