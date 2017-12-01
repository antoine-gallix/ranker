import pytest
from simple_profile import profile

# ----| fixtures


@pytest.fixture
def f():
    def function():
        pass
    return function


@pytest.fixture
def g():
    def function():
        pass
    return function

# ----| tests


def test_setup_profile(f):
    f = profile(f)
    f()


def test_count_calls(f):
    f = profile(f)
    assert f.count_calls() == 0
    f()
    f()
    assert f.count_calls() == 2


def test_count_calls_multiple_funtions(f, g):
    f = profile(f)
    g = profile(g)
    assert f.count_calls() == 0
    assert g.count_calls() == 0
    f()
    f()
    g()
    g()
    g()
    assert f.count_calls() == 2
    assert g.count_calls() == 3


def test_execution_times(f):
    f = profile(f)
    assert f.count_calls() == 0
    f()
    f()
    times = f.execution_times()
    assert len(times) == 2


def test_reset_profiles(f):
    f = profile(f)
    assert f.count_calls() == 0
    f()
    f()
    assert f.count_calls() == 2
    times = f.execution_times()
    assert len(times) == 2
    f.reset_profile()
    times = f.execution_times()
    assert len(times) == 0
    assert f.count_calls() == 0


def test_average_time(f):
    f = profile(f)
    f()
    f()
    avg = f.average_execution_time()
    assert avg > 0


def test_total_time(f):
    f = profile(f)
    f()
    f()
    tot = f.average_execution_time()
    assert tot > 0
