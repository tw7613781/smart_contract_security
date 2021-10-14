pragma solidity ^0.6.10;

contract EtherStore {
	mapping(address => uint) public balances;

	constructor() public payable {}

	function deposit() public payable {
		balances[msg.sender] += msg.value;
	}

	function withdraw(uint _amount) public {
		require(balances[msg.sender] >= _amount);
		
		(bool sent,) = msg.sender.call{value: _amount}("");
		require(sent, "Failed to send Ether");

		balances[msg.sender] -= _amount;
	}

	function getBalance() public view returns (uint) {
		return address(this).balance;
	}
}
