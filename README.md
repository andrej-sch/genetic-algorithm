# Genetic Algorithms for Unconstrained Single-Objective Optimization Problems



## 7. Integrated development environment

Task: _Use a good IDE and get fluent with it as e.g. IntelliJ. What are your favourite Key-Shortcuts?_

The project was developed in Micrisift Visual Code. It comes with a built-in IntelliSense facilitating code development. On top of that, additional plugins for Python were installed, enabling debugging and linting.

Often used shortcuts:

Combination | Description
--- | ---
`Ctrl+K Ctrl+O` | Open Folder (project)
`Ctrl+K F` | Close Folder (project)
`Ctrl+B` | Toggle Sidebar
`Ctrl+J` | Toggle Panel
`Ctrl+/` | Toggle Line Comment
`Ctrl+Z` | Toggle Word Wrap
`F11` | Toggle Full Screen
`F1` or `Ctrl+Shift+P`| Command Palette
`Ctrl+P` | Go to File..., Quick Open
`Ctrl+\` | Split Editor
`Ctrl+[n]` | Focus into _n_-th Editor Group
`Ctrl+F` | Find
`Ctrl+H` | Replace
`Alt+Down` | Move Line Down
`Alt+Up` | Move Line Up
`F9` | Toggle Breakpoint
`F5` | Start/Continue Debugging
`F11` | Step Into
`Shift+F11` | Step Out
`F10` | Step Over
`Shift+F5` | Stop

## 9. Functional Programming

Task: _Prove that you have covered all functional definitions in your code as:_

   - only final data structures
   - (mostly) side effect free functions
   - the use of higher order functions
   - functions as parameters and return values
   - use clojures / anonymous functions

Final data structures

Side effect free function

The use of higher order function can be found in the module `tools.py` functions `create_population` line 13, `_proportional_selection` line 131, `_rank_selection` line157, and `_two_point_crossover` line 241. As well as in the module `benchmark.py` functions `_function_3` line 159, `_function_4` line 175.

A closure can be found in the module `benchmark.py` line 73, definition of the function `_decode`, which in tern returns the internal function. The closure is being called in the same module in the function `get_scores` line 23.

Anonymous functions can be found in the module `utils.py` line 8 (function `swap`) and line 10 (function `square`).
