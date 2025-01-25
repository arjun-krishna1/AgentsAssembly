# AgentsAssembly
Create AI agents that represent your political preferences, you get funding tokens and your agent can direct your funding tokens towards projects allowing you to control how the government uses your taxes more directly

# Project Definition
The project is an AI voting agents to pass government projects
Voting agents
Project agents
Project agents have to convince voting agents to give them tokents
Tokens are used to fund the execution of the project
If citizen doesn’t vote by the project deadline
The agent chooses how many tokens to contribute
# Minimum Viable Product
Django web application
You can create your Voting agent with a list of your preferences
Project agents can be proposed
Humans can vote by the project deadline, if they don’t their voting agent votes as their representative
Chooses an amount of tokens to give to the project
Shows what votes your voting agent has done
=======
## Foundry

**Foundry is a blazing fast, portable and modular toolkit for Ethereum application development written in Rust.**

Foundry consists of:

-   **Forge**: Ethereum testing framework (like Truffle, Hardhat and DappTools).
-   **Cast**: Swiss army knife for interacting with EVM smart contracts, sending transactions and getting chain data.
-   **Anvil**: Local Ethereum node, akin to Ganache, Hardhat Network.
-   **Chisel**: Fast, utilitarian, and verbose solidity REPL.

## Documentation

https://book.getfoundry.sh/

## Usage

### Build

```shell
$ forge build
```

### Test

```shell
$ forge test
```

### Format

```shell
$ forge fmt
```

### Gas Snapshots

```shell
$ forge snapshot
```

### Anvil

```shell
$ anvil
```

### Deploy

```shell
$ forge script script/Counter.s.sol:CounterScript --rpc-url <your_rpc_url> --private-key <your_private_key>
```

### Cast

```shell
$ cast <subcommand>
```

### Help

```shell
$ forge --help
$ anvil --help
$ cast --help
```
