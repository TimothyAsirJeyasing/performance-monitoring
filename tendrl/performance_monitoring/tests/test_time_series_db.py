from ConfigParser import SafeConfigParser
from mock import MagicMock
import sys
sys.modules['tendrl.common.log'] = MagicMock()
from tendrl.performance_monitoring.time_series_db.dbplugins.graphite \
    import GraphitePlugin
from tendrl.performance_monitoring.time_series_db.manager \
    import TimeSeriesDBManager
del sys.modules['tendrl.common.log']


class TestTimeSeriesDbManager(object):
    def get_mock_config(self, db_name):
        cParser = SafeConfigParser()
        cParser.add_section('commons')
        cParser.set('commons', 'etcd_connection', '0.0.0.0')
        cParser.set('commons', 'etcd_port', '2379')
        cParser.add_section('time_series')
        cParser.set('time_series', 'time_series_db', db_name)
        cParser.set('time_series', 'time_series_db_server', '0.0.0.0')
        cParser.set('time_series', 'time_series_db_port', '80')
        return cParser

    def test_time_series_db_manager_sucess(self, monkeypatch):
        time_series_db_manager = TimeSeriesDBManager(
            self.get_mock_config('graphite'),
            'graphite'
        )
        assert isinstance(
            time_series_db_manager.get_plugin(),
            GraphitePlugin
        )
