from woke.testing import *
from pytypes.contracts.Counter import Counter


@default_chain.connect()
def test_counter():
    default_chain.set_default_accounts(default_chain.accounts[0])
    owner = default_chain.accounts[0]
    other = default_chain.accounts[1]

    counter = Counter.deploy(from_=owner)
    assert counter.count() == 0

    counter.increment(from_=other)
    assert counter.count() == 1


@default_chain.connect()
def test_whitelist():
    default_chain.set_default_accounts(default_chain.accounts[0])
    owner = default_chain.accounts[0]
    other = default_chain.accounts[1]

    counter = Counter.deploy(from_=owner)

    with must_revert():
        counter.setCount(20, from_=other)
    assert counter.count() == 0

    with must_revert():
        counter.addToWhitelist(other, from_=other)
    assert counter.count() == 0

    counter.addToWhitelist(other, from_=owner)
    assert counter.whitelist(other) == 1

    counter.setCount(20, from_=other)
    assert counter.count() == 20

    # does not increment
    counter.increment(request_type='call')
    assert counter.count() == 20

    # increment count by 1
    counter.increment(request_type='tx')
    assert counter.count() == 21

    gas_estimate = counter.increment(request_type="estimate")
