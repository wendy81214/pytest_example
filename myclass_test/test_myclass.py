import pytest


def test_add_age(person):
    assert isinstance(person.add_age(1), int)
    with pytest.raises(TypeError):
        person.add_age('wefwef')


def test_get_age(person):
    assert isinstance(person.get_age(), int)


def test_get_name(person):
    assert isinstance(person.get_name(), str)
    with pytest.raises(TypeError):
        person.get_name('')
