from brownie import (
    accounts,
    network,
    config,
    Contract,
    interface,
)

import eth_utils
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["ganache-local", "development"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def get_account(index=None, id=None):
    # account[0]
    # accounts.add("env")
    # account.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


DECIMALS = 8
INITIAL_VALUE = 200000000000


BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # tx = interface.LinkTokenInterface.transfer(
    #    contract_address, amount, {"from": account}
    # )
    tx.wait(1)
    print("fund contract")


def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    if proxy_admin_contract:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy,
                new_implementation_address,
                encoded_function_call,
                {"from": account},
            )
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy, new_implementation_address, {"from": account}
            )
    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                new_implementation_address,
                encoded_function_call,
                {"from": account},
            )
        else:
            transaction = proxy_admin_contract.upgrade(
                new_implementation_address, {"from": account}
            )
    return transaction
