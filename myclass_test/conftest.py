import pytest
from myclass.Person import Person


@pytest.fixture(scope = 'module')
def person():
    age = 19
    name = 'ken'
    #p = Person('ken', 19)
    yield Person('ken', 19)
