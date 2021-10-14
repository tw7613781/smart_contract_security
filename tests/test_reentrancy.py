import pytest
import brownie

@pytest.fixture(scope='module')
def alice(accounts):
    return accounts[0]

@pytest.fixture(scope='module')
def bob(accounts):
    return accounts[1]

@pytest.fixture(scope='module')
def eve(accounts):
    return accounts[2]

@pytest.fixture
def etherStore(EtherStore, alice, bob):
    etherStore = EtherStore.deploy({'from': alice})
    etherStore.deposit({'from': alice, 'value': '1 ether'})
    etherStore.deposit({'from': bob, 'value': '1 ether'})
    assert etherStore.getBalance() == '2 ether'
    return etherStore

@pytest.fixture
def attack(Attack, etherStore, alice):
    return Attack.deploy(etherStore.address, {'from': alice})

@pytest.fixture
def etherStoreSecure1(EtherStoreSecure1, alice, bob):
    etherStoreSecure1 = EtherStoreSecure1.deploy({'from': alice})
    etherStoreSecure1.deposit({'from': alice, 'value': '1 ether'})
    etherStoreSecure1.deposit({'from': bob, 'value': '1 ether'})
    assert etherStoreSecure1.getBalance() == '2 ether'
    return etherStoreSecure1

@pytest.fixture
def attack1(Attack, etherStoreSecure1, alice):
    return Attack.deploy(etherStoreSecure1.address, {'from': alice})

@pytest.fixture
def etherStoreSecure2(EtherStoreSecure2, alice, bob):
    etherStoreSecure2 = EtherStoreSecure2.deploy({'from': alice})
    etherStoreSecure2.deposit({'from': alice, 'value': '1 ether'})
    etherStoreSecure2.deposit({'from': bob, 'value': '1 ether'})
    assert etherStoreSecure2.getBalance() == '2 ether'
    return etherStoreSecure2

@pytest.fixture
def attack2(Attack, etherStoreSecure2, alice):
    return Attack.deploy(etherStoreSecure2.address, {'from': alice})


def test_normal_usage(etherStore, eve):
    assert etherStore.balances(eve) == 0
    etherStore.deposit({'from': eve, 'value': '1 ether'})
    assert etherStore.getBalance() == '3 ether'
    assert etherStore.balances(eve) == '1 ether'
    etherStore.withdraw('1 ether', {'from': eve})
    assert etherStore.getBalance() == '2 ether'
    assert etherStore.balances(eve) == 0

def test_reentrancy_attack(etherStore, attack, eve):
    assert etherStore.balances(eve) == 0
    attack.attack({'from': eve, 'value': '1 ether'})
    assert etherStore.getBalance() == 0
    assert etherStore.balances(eve) == 0
    assert attack.getBalance() == '3 ether'

def test_normal_usage_secure1(etherStoreSecure1, eve):
    assert etherStoreSecure1.balances(eve) == 0
    etherStoreSecure1.deposit({'from': eve, 'value': '1 ether'})
    assert etherStoreSecure1.getBalance() == '3 ether'
    assert etherStoreSecure1.balances(eve) == '1 ether'
    etherStoreSecure1.withdraw('1 ether', {'from': eve})
    assert etherStoreSecure1.getBalance() == '2 ether'
    assert etherStoreSecure1.balances(eve) == 0

def test_reentrancy_secure1_attack(etherStoreSecure1, attack1, eve):
    assert etherStoreSecure1.balances(eve) == 0
    with brownie.reverts('Failed to send Ether'):
        attack1.attack({'from': eve, 'value': '1 ether'})

def test_normal_usage_secure2(etherStoreSecure2, eve):
    assert etherStoreSecure2.balances(eve) == 0
    etherStoreSecure2.deposit({'from': eve, 'value': '1 ether'})
    assert etherStoreSecure2.getBalance() == '3 ether'
    assert etherStoreSecure2.balances(eve) == '1 ether'
    etherStoreSecure2.withdraw('1 ether', {'from': eve})
    assert etherStoreSecure2.getBalance() == '2 ether'
    assert etherStoreSecure2.balances(eve) == 0

def test_reentrancy_secure2_attack(etherStoreSecure2, attack2, eve):
    assert etherStoreSecure2.balances(eve) == 0
    with brownie.reverts('Failed to send Ether'):
        attack2.attack({'from': eve, 'value': '1 ether'})