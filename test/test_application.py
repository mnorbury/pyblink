import mock

from application import Controller


@mock.MagicMock(spec='datasource.DataSource')
def test_call_data_source(datasource):
    application = Controller(datasource)

    application

    datasource.assert_called