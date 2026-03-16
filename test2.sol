// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Reentrancy {
    mapping(address => uint) balances;
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
}