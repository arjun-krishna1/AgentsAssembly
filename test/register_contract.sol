// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import { ISPGNFT } from "@storyprotocol/periphery/interfaces/ISPGNFT.sol";

contract GovernmentProjectFund {
    address public spgNFTImplementation;

    // Event emitted when the contract is registered
    event ContractRegistered(address indexed contractAddress, string name, string symbol);

    constructor(address _spgNFTImplementation) {
        require(_spgNFTImplementation != address(0), "Invalid implementation address");
        spgNFTImplementation = _spgNFTImplementation;
    }

    // Function to register the contract on Story Protocol
    function registerProject(
        string memory name,
        string memory symbol,
        string memory baseURI,
        string memory contractURI,
        uint32 maxSupply,
        uint256 mintFee,
        address mintFeeToken,
        address mintFeeRecipient,
        bool mintOpen,
        bool isPublicMinting
    ) public {
        // Prepare the initialization parameters
        ISPGNFT.InitParams memory initParams = ISPGNFT.InitParams({
            name: name,
            symbol: symbol,
            baseURI: baseURI,
            contractURI: contractURI,
            maxSupply: maxSupply,
            mintFee: mintFee,
            mintFeeToken: mintFeeToken,
            mintFeeRecipient: mintFeeRecipient,
            owner: address(this),
            mintOpen: mintOpen,
            isPublicMinting: isPublicMinting
        });

        // Deploy and initialize the SPG NFT contract
        ISPGNFT SPG_NFT =ISPGNFT(spgNFTImplementation);
        SPG_NFT.initialize(initParams);
        address deployedContract = ;

        // Emit an event for transparency
        emit ContractRegistered(deployedContract, name, symbol);
    }
}