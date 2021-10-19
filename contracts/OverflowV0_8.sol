pragma solidity ^0.8.9;

contract OverflowIntermediateValueV0_8 {
    function testOverflow() public pure returns (uint){
        uint max_uint = 2 ** 256 - 1;
        return max_uint * 2 / 3;
    }
}