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
    console.log(`Creating clinet.`);
    const client = StoryClient.newClient(config)
    console.log(`Client Created`);

    const payRoyalty = await client.royalty.payRoyaltyOnBehalf({
        receiverIpId: '0x1eB0CDa81cEe4843927d04705eCcF1Dc327fC75F', // child ipId
        payerIpId: zeroAddress,
        token: "0xC0F6E387aC0B324Ec18EAcf22EE7271207dCE3d5", // insert SUSD address from https://docs.story.foundation/docs/deployed-smart-contracts
        amount: 1,
        txOptions: { waitForTransaction: true },
    })

    console.log(`Paid royalty at transaction hash ${payRoyalty.txHash}`)
}

main();

