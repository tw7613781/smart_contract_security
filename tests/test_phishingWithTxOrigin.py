import pytest
import brownie

@pytest.fixture(scope='module')
def alice(accounts):
    return accounts[0]

@pytest.fixture(scope='module')
def bob(accounts):
    return accounts[1]

@pytest.fixture
def wallet(WalletWithTxOrigin, alice):
    return WalletWithTxOrigin.deploy({'from': alice})

@pytest.fixture
def attack1(AttackTxOrigin, wallet, bob):
    return AttackTxOrigin.deploy(wallet, {'from': bob})    

def test_phishing(wallet, attack1, alice, bob):
    # Alice deposit 1 ether to wallet contract
    wallet.deposit({'from': alice, 'value': '1 ether'})
    assert wallet.getBalance() == '1 ether'

    # Bob attack the wallet contract but failed
    with brownie.reverts('Not owner'):
        attack1.attack({'from': bob})

    # Alice mis-called the attack function by cyber phishing
    # bob got all the balance of wallet contract
    bobBalanceBeforeAttack = bob.balance()
    tx = attack1.attack({'from': alice})
    print(tx.events)
    assert bob.balance() - bobBalanceBeforeAttack == '1 ether'