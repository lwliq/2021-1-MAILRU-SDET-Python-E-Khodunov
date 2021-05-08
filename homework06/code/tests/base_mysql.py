import os
import pytest

from mysql.builder import MySQLBuilder
from utils.log_parser import parse_log


class MySQLBase:

    def prepare(self):
        pass

    def get_file_path(self, file_name):
        return os.path.join(self.repo_root, 'tests', 'files', file_name)

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, repo_root):
        self.mysql = mysql_client
        self.repo_root = repo_root
        self.mysql_builder = MySQLBuilder(mysql_client)

        self.parsed_log = parse_log(self.get_file_path('access.log'))

        self.prepare()
