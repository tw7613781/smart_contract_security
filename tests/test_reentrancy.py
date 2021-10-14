import pytest

@pytest.fixture(scope='module')
def alice(accounts):
    return accounts[0]

@pytest.fixture(scope='module')
def bob(accounts):
    return accounts[1]

@pytest.fixture
def etherStore(EtherStore, alice):
    return EtherStore.deploy({'from': alice, 'value': '100 ether'})

def test_normal_usage(etherStore, bob):
    assert etherStore.getBalance() == '100 ether'
    assert etherStore.balances(bob) == 0
    etherStore.deposit({'from': bob, 'value': '5 ether'})
    assert etherStore.getBalance() == '105 ether'
    assert etherStore.balances(bob) == '5 ether'


