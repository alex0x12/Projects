# Project: Parser for math expressions
## Method: Reverse polish notation (postfix notation) 
- This project gives an example how to easily process math expressions using <ins>stack</ins>.

The program takes string input and converts it to postfix expression via [Shunting Yard Algorithm](https://en.wikipedia.org/wiki/Shunting_yard_algorithm).\
The input must be grammatically correct as there is no preprocessing yet, but only lexer and parser.\
As a result, we get a string that's ready to be counted.

## Example
![work_example](rs.png)

## TODO
- Preprocessing 
- Calculation 

## Build options
```console
  CFLAGS_DEBUG="-Werror -Wall -Wextra -DDEBUG -g"
  CFLAGS_RELEASE="-Werror -Wall -Wextra"
  for item in $PWD/*.c; do
    [ "$1" == "-release" ] && \
    gcc -c $CFLAGS_RELEASE $item || \
    gcc -c $CFLAGS_DEBUG $item
  done
  gcc rpn.o rpn_utils.o -lm -o rpn
```
