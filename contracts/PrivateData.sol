pragma solidity ^0.6.10;

contract Vault {
	// slot 0
	uint public count = 123; // uint is uint256 => 32 bytes

	// slot 1
	address public owner = msg.sender; // 20 bytes
	bool public isTrue = true; // 1 byte
	uint16 public u16 = 31; // 2 bytes

	// slot 2
	bytes32 private password; // 32 bytes

	// constants do not use storage, it hard coded into bytecode of contract
	uint public constant someConst = 123;

	// slot 3,4,5 (one for each array element)}
	bytes32[3] public data;

	struct User {
		uint id;
		bytes32 password;
	}

	// slot 6 - length of unbound array
	// so the users.length is easy to obtain in solidity
	// the real data of unbound array stored in keccak256(slot) + (index * elementSize)
	// where slot = 6 and elementSize = 2
	User[] private users;

	// slot 7 - empty
	// mapping doesn't store the data length
	// entries are stored at keccak256(key, slot)
	// where slot = 7, key = map key
	mapping(uint => User) private idToUser;

	constructor(bytes32 _password) public {
		password = _password;
	}

	function addUser(bytes32 _password) public {
		User memory user = User({
			id: users.length,
			password: _password
		});

		users.push(user);
		idToUser[user.id] = user;
	}

	function getArrayLocation(uint slot, uint index, uint elementSize) public pure returns (uint) {
		return uint(keccak256(abi.encodePacked(slot))) + (index * elementSize);
	}

	function getMapLocation(uint slot, uint key) public pure returns (uint) {
		return uint(keccak256(abi.encodePacked(key, slot)));
	}
}
