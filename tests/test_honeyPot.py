import pytest
import brownie

@pytest.fixture(scope='module')
def alice(accounts):
    return accounts[0]

@pytest.fixture(scope='module')
def bob(accounts):
    return accounts[1]

@pytest.fixture
def honeyPot(HoneyPot, alice):
    return HoneyPot.deploy({'from': alice})

@pytest.fixture
def bank(Bank, honeyPot, alice):
    return Bank.deploy(honeyPot, {'from': alice})

@pytest.fixture
def attack1(AttackHoneyPot, bank, bob):
    return AttackHoneyPot.deploy(bank, {'from': bob})    

def test_honeyPot(bank, attack1, alice, bob):
    # Alice deposit 1 ether to bank contract
    bank.deposit({'from': alice, 'value': '1 ether'})
    assert bank.balance() == '1 ether'

    # Bob attack the wallet contract but get catched
    with brownie.reverts():
        tx = attack1.attack({'from': bob, 'value': '1 ether'})
        print(tx)
