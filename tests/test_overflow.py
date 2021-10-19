import pytest
import brownie

@pytest.fixture(scope='module')
def alice(accounts):
    return accounts[0]

@pytest.fixture(scope='module')
def bob(accounts):
    return accounts[1]

@pytest.fixture
def timeLock(TimeLock, alice):
    return TimeLock.deploy({'from': alice})

@pytest.fixture
def attack(OverflowAttack, timeLock, alice):
    return OverflowAttack.deploy(timeLock, {'from': alice})

@pytest.fixture
def timeLockSecure(TimeLockSecure, alice):
    return TimeLockSecure.deploy({'from': alice})

@pytest.fixture
def attackSecure(OverflowAttack, timeLockSecure, alice):
    return OverflowAttack.deploy(timeLockSecure, {'from': alice})

@pytest.fixture
def overflowIntermediateValue(OverflowIntermediateValue, alice):
    return OverflowIntermediateValue.deploy({'from': alice})

@pytest.fixture
def overflowIntermediateValueV0_8(OverflowIntermediateValueV0_8, alice):
    return OverflowIntermediateValueV0_8.deploy({'from': alice})

def test_normal_useage(timeLock, alice):
    timeLock.deposit({'from': alice, 'value': '1 ether'})
    with brownie.reverts('Lock time not expired'):
        timeLock.withdraw({'from': alice})

def test_attack(attack, alice):
    tx = attack.attack({'from': alice, 'value': '1 ether'})
    print(tx.events)
    assert attack.balance() == '1 ether'

def test_attackSecure(attackSecure, alice):
    with brownie.reverts('SafeMath: addition overflow'):
        attackSecure.attack({'from': alice, 'value': '1 ether'})

def test_intermidiateOverflow(overflowIntermediateValue):
    with brownie.reverts('SafeMath: addition overflow'):
        overflowIntermediateValue.testOverflow()

def test_intermidiateOverflow0_8(overflowIntermediateValueV0_8):
    with brownie.reverts():
        overflowIntermediateValueV0_8.testOverflow()