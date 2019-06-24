# Typed Lambda Calculus in Python

## Setting up Environment

### Ubuntu Linux

Install pip.
```
$ sudo apt install python3-pip
```

Install Python's ply library.
```
$ pip3 install ply
```

### Mac


Use homebrew to install pip.
```
$ brew install python3
$ brew install pip3
```

Install ply.
```
$ pip3 install ply
```


## Fetching Source

Clone the repository from GitHub.
```
$ git clone https://github.com/ytakano/pytylambda.git
$ cd pytylambda
```

## Executing

Execute as follows.
```
$ python3 infer.py ./examples/ex04.lambda
Expression:
fun x { succ(x) }

AST:
['lambda',
 {'column': 1, 'line': 1},
 ['var', {'column': 5, 'line': 1}, 'x'],
 ['succ', {'column': 9, 'line': 1}, ['var', {'column': 14, 'line': 1}, 'x']]]

Typed AST:
[['T1', 'int'],
 ['lambda',
  {'column': 1, 'line': 1},
  ['var', {'column': 5, 'line': 1}, 'x'],
  ['int',
   ['succ',
    {'column': 9, 'line': 1},
    ['T1', ['var', {'column': 14, 'line': 1}, 'x']]]]]]

Type Constraint:
[['T1', 'int']]

Type Environment:
{'x': 'T1'}
```

## Examples

There are some examples in the examples directory.

```
$ ls examples
ex01.lambda  ex02.lambda  ex03.lambda  ex04.lambda
```

## Grammer

```
VAR := [a-zA-Z][a-zA-Z0-1]*
EXP := fun $VAR { $EXP }                   |
       if $EXP then { $EXP } else { $EXP } |
       $EXP ( $EXP )                       |
       iszero ( $EXP )                     |
       pred ( $EXP )                       |
       succ ( $EXP )                       |
       true                                |
       false                               |
       ( $EXP )                            |
       $VAR
```