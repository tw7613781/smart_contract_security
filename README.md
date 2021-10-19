# Known security issues and implementation

## Intro

The contracts are written in solidity and tested with Brownie framework. Python virtual environment and dependencies is managed by Poetry.

The contracts are from [Youtube Channel Smart Contract Programmer](https://www.youtube.com/watch?v=4Mm3BCyHtDY&list=PLO5VPQH6OWdWsCgXJT9UuzgbC8SPvTRi5)

Security issues

- Reentrancy

repeatedly calling some certain functions

- Arithmetci Overflow and Underflow

uint256 range from `[0, 2**256 - 1]`, the solidity natively doesn't handle overflow or underflow error. if exceeds the maximum number, the result will go from the begin. for example. `2**256 - 1 + 1 = 0`

> Solidity 0.8 release notes: Arithmetic operations revert on underflow and overflow. You can use unchecked { ... } to use the previous wrapping behaviour. Checks for overflow are very common, so we made them the default to increase readability of code, even if it comes at a slight increase of gas costs.

- Force Send Ether with selfdestruct

selfdestruct() function will delete the current contract from blockchain. Before be deleted, the contract will sent it's balance ether to a specific payable address which is the parameter of the selfdestruct function.

```solidity
selfdestruct(address payable _to)
```

## How to run the test

prerequisite: Poetry

```
# create virtual env and install dependencies
poetry install

# go into virtual env 
poetry shell
# or
source {path_to_venv}/bin/activate
```

```
# -s could see debug info
<venv>brownie test [-s]
```
