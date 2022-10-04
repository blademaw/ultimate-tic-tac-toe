# ultimate-tic-tac-toe

A small project in exploring strategies, heuristics, and learning techniques for the two-player board game Ultimate tic-tac-toe.

## Description
[Ultimate tic-tac-toe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe) is a variant of the popular two-player game tic-tac-toe &mdash; it is essentially a nested version of the original: with nine local boards and a single global board, players make a move on a local board, sending the next player to play on the corresponding global board cell's local board. To win a global board cell, players must win that square's local board. The game terminates according to normal tic-tac-toe rules with respect to the global board.

Ultimate tic-tac-toe has [two popular rulesets](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe#Rules), which differ in what happens when a player sends another player to an already-won/tied global square. For one ruleset there is a [proven winning strategy](https://arxiv.org/abs/2006.02353v2) &mdash; for this project I have adopted the other, more interesting ruleset, which has a larger search space and no well-defined strategy.

## Usage

Run `ultimatettt_runner.py` to run a game between two players &mdash; by default this runs a single game between two random agents (`randomAgent.py`), which select random legal moves.

### Command line

To customize parameters of the game, the following options are available at the time of writing (though `-h` is recommended for delayed README changes):

* `-h`: get flags for `ultimatettt_runner.py`
* `-a`: specify agents to compete against each other
* `-n`: specify agent names
* `-p`: print game states at each agent move as a text-rendered board
* `-g`: number of games to run
* `-d`: debug (print verbose agent information)
* `-r`: render board at each move as PNGs
* `-f`: save a replay of the game with a provided filetype (GIF is preferred)

For example, running

```bash
$ python ultimatettt_runner.py -a agents.mctsAgent,agents.randomAgent -g 1 -p -r -f gif
```

will run one game of the MCTS agent versus the random agent, printing the game states at each step, as well as rendering each move as an image file and producing a GIF replay of the game.

### Agents

Agents are implemented with the `Agent` class from `agents/agent.py`. Each agent must have a way to select a move (`selectAction(...)`).

### Display options

#### Text rendering

The board can be printed at each move in a text environment, resulting in the following example output:

```
Move 56: Agent #2 (X) to play:

                 |               |
     X | O | X   |               |
    ———|———|———  |               |
       | X | O   |       X       |       X
    ———|———|———  |               |
       | O | O   |               |
                 |               |
—————————————————|———————————————|—————————————————
                 |               |
     X | X | O   |               |     | O | O
    ———|———|———  |               |  ———|———|———
       |   | X   |       O       |   X |   |
    ———|———|———  |               |  ———|———|———
       | O | O   |               |   O | O | X
                 |               |
—————————————————|———————————————|—————————————————
                 |               |
                 |   X | O | O   |
                 |  ———|———|———  |
         X       |   O | X | X   |       X
                 |  ———|———|———  |
                 |   X | X |     |
                 |               |

Agent randomAgent chooses square 0, cell (2,0).

Move 57: Agent #1 (O) to play:

                 |               |
                 |               |
                 |               |
         O       |       X       |       X
                 |               |
                 |               |
                 |               |
—————————————————|———————————————|—————————————————
                 |               |
     X | X | O   |               |     | O | O
    ———|———|———  |               |  ———|———|———
       |   | X   |       O       |   X |   |
    ———|———|———  |               |  ———|———|———
       | O | O   |               |   O | O | X
                 |               |
—————————————————|———————————————|—————————————————
                 |               |
                 |   X | O | O   |
                 |  ———|———|———  |
         X       |   O | X | X   |       X
                 |  ———|———|———  |
                 |   X | X |     |
                 |               |

Agent mctsAgent chooses square 7, cell (2,2).

Move 58: Agent #2 (X) to play:

                 |               |
                 |               |
                 |               |
         O       |       X       |       X
                 |               |
                 |               |
                 |               |
—————————————————|———————————————|—————————————————
                 |               |
     X | X | O   |               |     | O | O
    ———|———|———  |               |  ———|———|———
       |   | X   |       O       |   X |   |
    ———|———|———  |               |  ———|———|———
       | O | O   |               |   O | O | X
                 |               |
—————————————————|———————————————|—————————————————
                 |               |
                 |               |
                 |               |
         X       |       X       |       X
                 |               |
                 |               |
                 |               |

Game 1 Result:
        Agent 0: mctsAgent wins.

Results for 1 games:
        Agent 0 mctsAgent won 1 games (100.0%) in an average 29.0 moves.
        Agent 1 randomAgent won 0 games (0.0%) in an average 29.0 moves.
```

#### Graphical rendering

Games can also be outputted as PNGs at each move &mdash; if an agent returns an _action-reward_ dictionary along with their selected action during the `selectAction()` call, this will be mapped to the game board (in the form of color and text). Graphical rendering is currently accomplished by plotting custom Seaborn heatmaps and saving figures.

For example, a random agent conducts no reward calculation, so the resulting graphical output for a random agent's turn may look like the following:

<img src="img\random_graphical.png" style="zoom:67%;" />

where the dark grey squares represent possible moves.

An agent such as `mctsAgent.py` can return an action-reward dictionary, so it will be mapped to the render (in this case, following the above random agent's move):

<img src="img\mcts_graphical.png" style="zoom:67%;" />

#### Graphical game replays

With the `-f <filetype>` option, games can be saved to GIFs/other files to produce a replay, such as the following:

<img src="img\ex_replay.gif" style="zoom:67%;" />

## Built with

* `numpy` for board representation
* `seaborn`, `matplotlib ` for graphical rendering
* `imageio` for GIF creation



### Acknowledgements

* The MCTS algorithm used in `mctsAgent.py` extends code from `mcts` by [pbsinclair42](https://github.com/pbsinclair42/MCTS) to allow for retrieval of agent-specific rewards and the action-reward dictionary.
* This project was inspired by a class I took involving AI planning strategies &mdash; the general architecture for the ultimate tic-tac-toe game representation in `ultimatettt_model.py` was largely inspired by code from this class, and therefore adapts work from Steven Spratley and Guang Ho from the University of Melbourne.