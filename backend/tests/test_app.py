import pytest
from app import app

@pytest.mark.skip(reason="TDD")
def test_always_passes():
    assert True

@pytest.mark.skip(reason="TDD")    
def test_always_fails():
    assert False
    
@pytest.mark.skip(reason="TDD")
def test_always_passes_2():
    assert 4 > 3