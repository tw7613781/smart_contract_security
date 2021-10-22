import pytest
from brownie.network import web3

@pytest.fixture(scope='module')
def alice(accounts):
    return accounts[0]

@pytest.fixture(scope='module')
def bob(accounts):
    return accounts[1]

@pytest.fixture
def lib1(HackMeLib1, alice):
    return HackMeLib1.deploy({'from': alice})

@pytest.fixture
def hackMe1(HackMe1, lib1, alice):
    return HackMe1.deploy(lib1.address, {'from': alice})

@pytest.fixture
def attack1(DelegateCallAttack1, hackMe1, alice):
    return DelegateCallAttack1.deploy(hackMe1.address, {'from': alice})

def test_hack_ownership(hackMe1, attack1, alice, bob):
    assert hackMe1.owner() == alice
    attack1.attack({'from': bob})
    assert hackMe1.owner() == attack1.address