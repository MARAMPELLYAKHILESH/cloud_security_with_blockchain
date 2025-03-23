// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MasterHashStorage {
    // Mapping from file identifier to master hash
    mapping(string => string) public masterHashes;

    event MasterHashStored(string fileId, string masterHash);

    // Function to store a master hash for a file
    function storeMasterHash(string memory fileId, string memory masterHash) public {
        masterHashes[fileId] = masterHash;
        emit MasterHashStored(fileId, masterHash);
    }

    // Function to retrieve the master hash for a file
    function getMasterHash(string memory fileId) public view returns (string memory) {
        return masterHashes[fileId];
    }
}
