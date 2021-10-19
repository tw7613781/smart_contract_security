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
def etherGame(EtherGame, alice):
    return EtherGame.deploy({'from': alice})

@pytest.fixture
def attack(EtherGameAttack, alice):
    return EtherGameAttack.deploy({'from': alice})

@pytest.fixture
def etherGameSecure(EtherGameSecure, alice):
    return EtherGameSecure.deploy({'from': alice})

def test_normal_useage(etherGame, alice, bob, eve):
    print(f'before game, eve balance is {eve.balance()}')

    etherGame.deposit({'from': alice, 'value': '1 ether'})
    etherGame.deposit({'from': bob, 'value': '1 ether'})
    etherGame.deposit({'from': eve, 'value': '1 ether'})
    etherGame.deposit({'from': eve, 'value': '1 ether'})
    etherGame.deposit({'from': bob, 'value': '1 ether'})
    etherGame.deposit({'from': alice, 'value': '1 ether'})
    etherGame.deposit({'from': eve, 'value': '1 ether'})

    assert etherGame.winner() == eve

    with brownie.reverts('Not winner'):
        etherGame.claimReward({'from': alice})    

    etherGame.claimReward({'from': eve})
    print(f'after the game, eve balance is {eve.balance()}')

def test_attack(etherGame, attack, alice, bob, eve):
    etherGame.deposit({'from': alice, 'value': '1 ether'})
    etherGame.deposit({'from': bob, 'value': '1 ether'})
    etherGame.deposit({'from': eve, 'value': '1 ether'})
    attack.attack(etherGame.address, {'from': alice, 'value': '4 ether'})
    with brownie.reverts('Game is over'):
        etherGame.deposit({'from': eve, 'value': '1 ether'})

def test_attackSecure(etherGameSecure, attack, alice, bob, eve):
    etherGameSecure.deposit({'from': alice, 'value': '1 ether'})
    etherGameSecure.deposit({'from': bob, 'value': '1 ether'})
    etherGameSecure.deposit({'from': eve, 'value': '1 ether'})
    attack.attack(etherGameSecure.address, {'from': alice, 'value': '4 ether'})
    etherGameSecure.deposit({'from': eve, 'value': '1 ether'})
    etherGameSecure.deposit({'from': bob, 'value': '1 ether'})
    etherGameSecure.deposit({'from': alice, 'value': '1 ether'})
    etherGameSecure.deposit({'from': eve, 'value': '1 ether'})

    assert etherGameSecure.winner() == eve