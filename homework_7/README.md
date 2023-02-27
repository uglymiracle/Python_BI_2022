# Python_BI_2022

## Homework #7

This homework is done without using packages

This homework is exercises to get skill in functional programming in Python

### Functions
`sequential_map` - takes any functions and data container. Output: result of sequential execution of all functions for this data

`consensus_filter` - takes any functions, which return True or False, and data container. Output: elements from data container, which have only True output from all functions

`conditional_reduce` - takes two functions. First function returns True or False. Second function takes 2 arguments and return only one value. Output: value from second function, which works with data after filtering by first function

`func_chain` - takes any functions and returns function, which sequential execute of all taked functions

`multiple_partial` - takes any functions and arguments for them and returns a list of the same number of "partial functions"