pragma solidity ^0.6.10;

contract EtherGame {
	uint public targetAmount = 7 ether;
	address public winner;

	function deposit() public payable {
		require(msg.value == 1 ether, "You can only send 1 Ether");

		uint balance = address(this).balance;
		require(balance <= targetAmount, "Game is over");

		if (balance == targetAmount) {
			winner = msg.sender;
		}
	}

	function claimReward() public {
		require(msg.sender == winner, "Not winner");

		(bool sent, ) = msg.sender.call{value: address(this).balance}("");
		require(sent, "Failed to send Ether");
	}

	function getBalance() public view returns (uint) {
		return address(this).balance;
	}
}

contract EtherGameAttack {
	function attack(address payable target) public payable {
		selfdestruct(target);
	}
}

contract EtherGameSecure {
	uint public targetAmount = 7 ether;
	address public winner;
	uint public balance;

	function deposit() public payable {
		require(msg.value == 1 ether, "You can only send 1 Ether");

		balance += msg.value;
		require(balance <= targetAmount, "Game is over");

		if (balance == targetAmount) {
			winner = msg.sender;
		}
	}

	function claimReward() public {
		require(msg.sender == winner, "Not winner");

		(bool sent, ) = msg.sender.call{value: address(this).balance}("");
		require(sent, "Failed to send Ether");
	}

	function getBalance() public view returns (uint) {
		return address(this).balance;
	}
}


