
from database import database_handler

from unittest import mock
from unittest.mock import MagicMock, Mock
import unittest


class DatabaseHandlerTest(unittest.TestCase):
    
    @mock.patch.object(database_handler,'cursor')
    def test_query(self, mock_cur):
        logger = Mock()
        conf = Mock()
        db = database_handler(logger,conf)
        db.connect = MagicMock(name='connect')
        db.execute_sql_query('SELECT table_name FROM information_schema.tables WHERE table_schema=\'public\'')
        mock_cur.assert_called_with('SELECT table_name FROM information_schema.tables WHERE table_schema=\'public\'')


if __name__ == '__main__':
    unittest.main()