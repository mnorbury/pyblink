from nose.tools import eq_

from jenkins_monitor import aggregate

def _create_data( state_list ):
    return [dict(color=x) for x in state_list]

def test_all_green():
    data   = _create_data([ 'blue' , 'blue' ])

    result = aggregate( data )

    eq_(result, 'blue')

def test_one_yellow():
    data = _create_data([ 'blue' , 'yellow' ])

    result = aggregate( data )

    eq_(result, 'yellow')

def test_one_yellow_building():
    data = _create_data([ 'blue', 'yellow_anime' ])

    result = aggregate( data )

    eq_(result, 'yellow')

def test_one_red():
    data = _create_data([ 'blue', 'red' ])

    result = aggregate( data )

    eq_(result, 'red')

def test_grey_if_states_not_known():
    data = _create_data([ 'black', 'pink' ])

    result = aggregate( data )

    eq_(result, 'grey')
