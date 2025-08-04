// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DonorAllocationSmartContract {
    struct Allocation {
        address donor;
        address recipient;
        bool isVerified;
        uint256 expiry;
    }

    mapping(bytes32 => Allocation) public allocations;

    event DonorAllocated(bytes32 token, address donor, address recipient, uint256 expiry);
    event DonorVerified(bytes32 token);

    function allocateDonorToRecipient(address _donor, address _recipient) public returns (bytes32) {
        bytes32 token = keccak256(abi.encodePacked(_donor, _recipient, block.timestamp));
        allocations[token] = Allocation(_donor, _recipient, false, block.timestamp + 86400);
        emit DonorAllocated(token, _donor, _recipient, allocations[token].expiry);
        return token;
    }

    function verifyDonation(bytes32 token) public {
        Allocation storage alloc = allocations[token];
        require(msg.sender == alloc.donor, "Only donor can verify");
        require(!alloc.isVerified, "Already verified");
        require(block.timestamp <= alloc.expiry, "Token expired");

        alloc.isVerified = true;
        emit DonorVerified(token);
    }

    function getAllocation(bytes32 token) public view returns (address, address, bool, uint256) {
        Allocation memory a = allocations[token];
        return (a.donor, a.recipient, a.isVerified, a.expiry);
    }
}
