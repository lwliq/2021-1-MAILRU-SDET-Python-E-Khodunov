from mysql.models import RequestsCount, RequestsCountByType, Top10MostFrequentLocations, Top5LocationsBySize, \
    Top5MostFrequentIps
from tests.base_mysql import MySQLBase


class TestRequestsCount(MySQLBase):

    def prepare(self):
        entry = self.mysql_builder.create_requests_count(self.parsed_log['Task 01'])
        self.mysql.session.add(entry)

    def test_requests_count(self):
        row = self.mysql.session.query(RequestsCount).first()
        assert row.count == 225133


class TestRequestsCountByType(MySQLBase):

    def prepare(self):
        for entry in self.parsed_log['Task 02']:
            entry = self.mysql_builder.create_requests_count_by_type(entry)
            self.mysql.session.add(entry)

    def test_requests_count_by_type(self):
        rows = self.mysql.session.query(RequestsCountByType).all()
        assert self.compare_models_to_dicts_by_count(rows, self.parsed_log['Task 02'])


class TestTop10MostFrequentLocations(MySQLBase):

    def prepare(self):
        for entry in self.parsed_log['Task 03']:
            entry = self.mysql_builder.create_top_10_most_frequent_locations(entry)
            self.mysql.session.add(entry)

    def test_top_10_most_frequent_locations(self):
        rows = self.mysql.session.query(Top10MostFrequentLocations).all()
        assert self.compare_models_to_dicts_by_count(rows, self.parsed_log['Task 03'])


class TestTop5LocationsBySize(MySQLBase):

    def prepare(self):
        for entry in self.parsed_log['Task 04']:
            entry = self.mysql_builder.create_top_5_locations_by_size(entry)
            self.mysql.session.add(entry)

    def test_top_5_locations_by_size(self):
        rows = self.mysql.session.query(Top5LocationsBySize).all()
        assert self.compare_models_to_dicts_by_size(rows, self.parsed_log['Task 04'])


class TestTop5MostFrequentIps(MySQLBase):

    def prepare(self):
        for entry in self.parsed_log['Task 05']:
            entry = self.mysql_builder.create_top_5_most_frequent_ips(entry)
            self.mysql.session.add(entry)

    def test_top_5_most_frequent_ips(self):
        rows = self.mysql.session.query(Top5MostFrequentIps).all()
        assert self.compare_models_to_dicts_by_count(rows, self.parsed_log['Task 05'])
