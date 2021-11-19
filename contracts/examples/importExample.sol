// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import '@openzeppelin/contracts/token/ERC20/IERC20.sol';

contract tokenss{
    
    //uint[] public status;
    IERC20 public wowToken;
    
    constructor() public{
    
        wowToken = IERC20(0xd9145CCE52D386f254917e481eB44e9943F39138);
        
    }
    //uint[]  status;
    function ArraPush(uint[] calldata id ) public returns(uint[] memory){

        uint[] memory  status;
        for(uint i = 0; i< id.length;i++){
            wowToken.transferFrom(msg.sender,address(this),111);
            status[i] = 1;
        }
        
        return status;
    }
}