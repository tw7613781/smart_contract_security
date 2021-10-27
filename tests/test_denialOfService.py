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
def kingOfEther(KingOfEther, alice):
    return KingOfEther.deploy({'from': alice})

@pytest.fixture
def kingOfEtherSecure(KingOfEtherSecure, alice):
    return KingOfEtherSecure.deploy({'from': alice})    

@pytest.fixture
def attack1(DOSAttack, eve):
    return DOSAttack.deploy({'from': eve})

def test_dos_attack(kingOfEther, attack1, alice, bob, eve):
    kingOfEther.claimThrone({'from': alice, 'value': '1 ether'})
    assert kingOfEther.king() == alice
    assert kingOfEther.getBalance() == '1 ether'
    print(f'Alice balance {alice.balance() / 1e18}')

    kingOfEther.claimThrone({'from': bob, 'value': '2 ether'})
    assert kingOfEther.king() == bob
    assert kingOfEther.getBalance() == '2 ether'
    print(f'Alice balance {alice.balance() / 1e18}')

    attack1.attack(kingOfEther.address, {'from': eve, 'value': '3 ether'})
    assert kingOfEther.king() == attack1.address
    assert kingOfEther.getBalance() == '3 ether'

    # the service is not responsible any more
    with brownie.reverts('Failed to send Ether'):
        kingOfEther.claimThrone({'from': alice, 'value': '4 ether'})

def test_dos_attack_protection(kingOfEtherSecure, attack1, alice, bob, eve):
    kingOfEtherSecure.claimThrone({'from': alice, 'value': '1 ether'})
    assert kingOfEtherSecure.king() == alice
    assert kingOfEtherSecure.getBalance() == '1 ether'
    print(f'Alice balance {alice.balance() / 1e18}')

    kingOfEtherSecure.claimThrone({'from': bob, 'value': '2 ether'})
    assert kingOfEtherSecure.king() == bob
    assert kingOfEtherSecure.getBalance() == '3 ether'
    print(f'Alice balance {alice.balance() / 1e18}')

    attack1.attack(kingOfEtherSecure.address, {'from': eve, 'value': '3 ether'})
    assert kingOfEtherSecure.king() == attack1.address
    assert kingOfEtherSecure.getBalance() == '6 ether'

    # the service is still functional
    kingOfEtherSecure.claimThrone({'from': alice, 'value': '4 ether'})
    assert kingOfEtherSecure.king() == alice
    assert kingOfEtherSecure.getBalance() == '10 ether'
    print(f'Alice balance {alice.balance() / 1e18}')

    kingOfEtherSecure.claimThrone({'from': bob, 'value': '5 ether'})
    
    kingOfEtherSecure.withdraw({'from': alice})
    print(f'Alice balance {alice.balance() / 1e18}')