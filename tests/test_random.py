import pytest
from brownie.network import web3

@pytest.fixture(scope='module')
def alice(accounts):
    return accounts[0]

@pytest.fixture(scope='module')
def bob(accounts):
    return accounts[1]

@pytest.fixture
def guessContract(GuessTheRandomNumber, alice):
    return GuessTheRandomNumber.deploy({'from': alice, 'value': '10 ether'})

@pytest.fixture
def attack(RandonAttack, bob):
    return RandonAttack.deploy({'from': bob})

def test_hack_random(guessContract, attack, alice, bob):
    assert guessContract.balance() == '10 ether'
    assert attack.balance() == 0
    tx = attack.attack(guessContract.address, {'from': bob})
    print(tx.events)
    assert attack.balance() == '1 ether'