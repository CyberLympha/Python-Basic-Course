import pytest
import my_module as mm

@pytest.mark.skip(reason='Not needed')
def test_init_check():
    assert 1==1
    print()
    assert mm.Manager('name', 'surname', 'managet', 37).name == 'name'


@pytest.mark.parametrize("age, result", [
    (-1, None), (0, None), 
    (10, 'name'), (20, 'name'), (40, 'name'), 
    (60, 'name'), (80, 'name'), (100, 'name'), 
    (110, None)])
def test_create_object(age, result):
    assert str(mm.Manager('name', 'surname', 'managet', age)) == 'name surname' if result else 'None'

def test_change_currency():
    manager = mm.Manager('name', 'surname', 'managet', 33, 'rub')
    manager.change_currency('xxx')
    assert manager.currency == 'rub'

    manager = mm.Manager('name', 'surname', 'managet', 33, 'rub')
    manager.change_currency('usd')
    assert manager.currency == 'usd'


@pytest.mark.xfail(raises=AttributeError)
def test_set_name():
    manager = mm.Manager('name', 'surname', 'managet', 33, 'rub')
    setattr(manager, 'name', 'sometext')

@pytest.mark.xfail(raises=AttributeError)
def test_set_surname():
    manager = mm.Manager('name', 'surname', 'managet', 33, 'rub')
    setattr(manager, 'surname', 'sometext')

@pytest.mark.xfail(raises=TypeError)
def test_set_age():
    manager = mm.Manager('name', 'surname', 'managet', 33, 'rub')
    setattr(manager, 'age', 'sometext')