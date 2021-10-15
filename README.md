# Known security issues and implementation

## Intro

The contracts are written in solidity and tested with Brownie framework.

The contracts are from [Youtube Channel Smart Contract Programmer](https://www.youtube.com/watch?v=4Mm3BCyHtDY&list=PLO5VPQH6OWdWsCgXJT9UuzgbC8SPvTRi5)

Security issues

- Reentrancy

repeatedly calling some certain functions

- Arithmetci Overflow and Underflow

uint256 range from `[0, 2**256 - 1]`, the solidity natively doesn't handle overflow or underflow error. if exceeds the maximum number, the result will go from the begin. for example. `2**256 - 1 + 1 = 0`

## How to run the test

prerequisite: brownie framwork

```
brownie test
```