from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import (
    network,
    Box,
    TransparentUpgradeableProxy,
    ProxyAdmin,
    Contract,
    BoxV2,
)
import time


def main():
    account = get_account()
    print(f"deploying from {network.show_active()}")
    box = Box.deploy({"from": account}, publish_source=True)
    # box.wait(1)
    print("box deployed")
    # vv = box.retrieve()
    # time.sleep(5)
    # vv.wait(1)
    # print(f"box value= {vv}")
    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=True)
    initializer = box.store, 1
    # constructor yok initilaz etmek gerekiyor 1 değişken alan fonk cagirdik gibi bisiler
    box_encoded_initializer_function = encode_function_data(initializer)
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
        publish_source=True,
    )
    print(f"proxy deployed at {proxy} !!")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    print(proxy_box)
    print(f"return {proxy_box.retrieve()}")
    proxy_box.store(2, {"from": account})
    # ret = proxy_box.retrieve({"from": account})
    print(f"return {proxy_box.retrieve()}")

    box_v2 = BoxV2.deploy({"from": account}, publish_source=True)
    upgrade_tx = upgrade(
        account, proxy, box_v2.address, proxy_admin_contract=proxy_admin
    )
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": account})
    print(f"return box2  {proxy_box.retrieve()}")
