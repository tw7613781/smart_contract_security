import pytest
from brownie.network import web3
from hexbytes import HexBytes

@pytest.fixture(scope='module')
def alice(accounts):
    return accounts[0]

@pytest.fixture
def vault(Vault, alice):
    return Vault.deploy(0x1234abc, {'from': alice})

def test_uint(vault):
    data = web3.eth.get_storage_at(vault.address, 0)
    assert data == HexBytes('0x7b')

def test_address(vault):
    data = web3.eth.get_storage_at(vault.address, 1)
    assert data == HexBytes('0x1f0166ab6d9362d4f35596279692f0251db635165871')

def test_private_data(vault):
    data = web3.eth.get_storage_at(vault.address, 2)
    assert data == HexBytes('0x01234abc')

def test_fix_size_array(vault):
    data = web3.eth.get_storage_at(vault.address, 3)
    assert data == HexBytes('0x0')

def test_unbound_array(vault):
    vault.addUser('12345')
    vault.addUser('abcd')
    data = web3.eth.get_storage_at(vault.address, 6)
    assert data == HexBytes('0x2')

    array_first_element_id_address = vault.getArrayLocation(6, 0, 2)
    array_first_element_password_address = vault.getArrayLocation(6, 0, 2) + 1

    data = web3.eth.get_storage_at(vault.address, array_first_element_id_address)
    assert data == HexBytes('0x0')

    data = web3.eth.get_storage_at(vault.address, array_first_element_password_address)
    assert data == HexBytes('0x12345')

def test_mapping(vault):
    vault.addUser('12345')
    vault.addUser('abcd')
    data = web3.eth.get_storage_at(vault.address, 7)
    assert data == HexBytes('0x0')

    array_second_element_id_address = vault.getMapLocation(7, 1)
    array_second_element_password_address = vault.getMapLocation(7, 1) + 1

    data = web3.eth.get_storage_at(vault.address, array_second_element_id_address)
    assert data == HexBytes('0x1')

    data = web3.eth.get_storage_at(vault.address, array_second_element_password_address)
    assert data == HexBytes('0xabcd')