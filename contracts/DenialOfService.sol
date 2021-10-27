pragma solidity ^0.6.10;

contract KingOfEther {
    address public king;
    uint public balance;

    function claimThrone() external payable {
        require(msg.value > balance, "Need to pay more to become the king");

        (bool sent, ) = king.call{value: balance}("");
        require(sent, "Failed to send Ether");

        balance = msg.value;
        king = msg.sender;
    }

    function getBalance() external view returns (uint) {
        return address(this).balance;
    }
}

contract DOSAttack {
    function attack(KingOfEther kingOfEther) public payable {
        kingOfEther.claimThrone{value: msg.value}();
    }
}

contract KingOfEtherSecure {
    address public king;
    uint public balance;
    mapping(address => uint) public balances;

    function claimThrone() external payable {
        require(msg.value > balance, "Need to pay more to become the king");

        balances[king] += balance;

        balance = msg.value;
        king = msg.sender;
    }

    function withdraw() public {
        require(msg.sender !=king, "Current king cannot withdraw");

        uint amount = balances[msg.sender];
        balances[msg.sender] = 0;

        (bool sent, ) = msg.sender.call{value: amount}("");
        require(sent, "Failed to send Ether");
    }

    function getBalance() external view returns (uint) {
        return address(this).balance;
    }
}