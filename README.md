# Known security issues and implementation

## Intro

The contracts are written in solidity and tested with Brownie framework. Python virtual environment and dependencies is managed by Poetry.

The contracts are from [Youtube Channel Smart Contract Programmer](https://www.youtube.com/watch?v=4Mm3BCyHtDY&list=PLO5VPQH6OWdWsCgXJT9UuzgbC8SPvTRi5)

### Security issues

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

- Private data

though private data can't be read directly by other contract or web3 API, the whole state variables (smart contract storage) can be read by `web3.eth.getStorageAt()`. Once known the source code of the contract, it's easy to calcalate the position of private data stored and conduct the value. So never store sensitive data in blockchain. 

contract stores it's state variables in order to the EMV storage, which is a list of 32 bytes long consecutive slots (space). The details please check the `PrivateData.sol` 

- delegatecall

there are two principles when create delegatecall function

1. run your code inside my context (storage, msg.sender, msg.value, msg.data, etc...)

2. storage layout must be the same for A and B.

if violate the two principles, it's easy to create bugs. 

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
