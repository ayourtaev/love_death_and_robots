import unittest
from unittest.mock import patch, mock_open


class RobotCoreTest(unittest.TestCase):

    def test_open_file(self):
        with patch('builtins.open', mock_open(read_data='data')) as mock_file:
            assert open('/').read() == 'data'
            mock_file.assert_called_with('/')


if __name__ == '__main__':
    unittest.main()
