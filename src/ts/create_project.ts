import { StoryClient, StoryConfig } from '@story-protocol/core-sdk'
import { http } from 'viem'
import { privateKeyToAccount, Address, Account } from 'viem/accounts'
import { PIL_TYPE } from '@story-protocol/core-sdk';
import { toHex, Address, zeroAddress } from 'viem';

const privateKey: Address = `0xf354996a7e2a9ca81d32825caff9abbdfbbe2f0033986dcaa01ee30fc3c9eb56`
export const account: Account = privateKeyToAccount(privateKey)

const config: StoryConfig = {
    account: account,
    transport: http(process.env.RPC_PROVIDER_URL),
    chainId: 'odyssey',
}
async function main() {
    const argv: minimist.ParsedArgs = require('minimist')(process.argv.slice(2));
    const client = StoryClient.newClient(config)
    const newCollection = await client.nftClient.createNFTCollection({
        name: argv['name'],
        symbol: 'LOCAL_PROJECT',
        isPublicMinting: false,
        mintOpen: true,
        mintFeeRecipient: "0xA5eAc45A53c8CEE1aBcb6a6F66aF81ea91303953",
        contractURI: '0x70a8BEB9158c6C3036eF3F4b175014d28BCd6ad2',
        txOptions: { waitForTransaction: true },
    })

    const response = await client.ipAsset.mintAndRegisterIp({
        // an NFT contract address created by the SPG
        spgNftContract: newCollection.spgNftContract as Address,
        // https://docs.story.foundation/docs/ip-asset#adding-nft--ip-metadata-to-ip-asset
        ipMetadata: {
            ipMetadataURI: 'test-uri',
            ipMetadataHash: toHex('test-metadata-hash', { size: 32 }),
            nftMetadataHash: toHex('test-nft-metadata-hash', { size: 32 }),
            nftMetadataURI: 'test-nft-uri',
        },
        txOptions: { waitForTransaction: true }
    });

    console.log(`${response.ipId}`);
}

main();