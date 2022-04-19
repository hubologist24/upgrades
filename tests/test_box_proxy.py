from scripts.helpful_scripts import get_account


from scripts.helpful_scripts import get_account, encode_function_data
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def test_can_proxy():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    initializer = box.store, 1
    # constructor yok initilaz etmek gerekiyor 1 değişken alan fonk cagirdik gibi bisiler
    box_encoded_initializer_function = encode_function_data(initializer)
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    assert proxy_box.retrieve() == 0
    proxy_box.store(1, {"from": account})
    assert proxy_box.retrieve() == 1
