from mysql.models import Task01, Task02, Task03, Task04, Task05
from tests.base_mysql import MySQLBase


class TestTask01(MySQLBase):

    def prepare(self):
        task01 = self.mysql_builder.create_task01_from_dict(self.parsed_log['Task 01'])
        self.mysql.session.add(task01)

    def test_task01(self):
        task01 = self.mysql.session.query(Task01).first()
        assert task01.count == 225133


class TestTask02(MySQLBase):

    def prepare(self):
        for entry in self.parsed_log['Task 02']:
            task02 = self.mysql_builder.create_task02_from_dict(entry)
            self.mysql.session.add(task02)

    def test_task02(self):
        task02 = self.mysql.session.query(Task02).all()
        assert len(task02) == 5


class TestTask03(MySQLBase):

    def prepare(self):
        for entry in self.parsed_log['Task 03']:
            task03 = self.mysql_builder.create_task03_from_dict(entry)
            self.mysql.session.add(task03)

    def test_task03(self):
        task03 = self.mysql.session.query(Task03).all()
        assert len(task03) == 10


class TestTask04(MySQLBase):

    def prepare(self):
        for entry in self.parsed_log['Task 04']:
            task04 = self.mysql_builder.create_task04_from_dict(entry)
            self.mysql.session.add(task04)

    def test_task04(self):
        task04 = self.mysql.session.query(Task04).all()
        assert len(task04) == 5


class TestTask05(MySQLBase):

    def prepare(self):
        for entry in self.parsed_log['Task 05']:
            task05 = self.mysql_builder.create_task05_from_dict(entry)
            self.mysql.session.add(task05)

    def test_task05(self):
        task05 = self.mysql.session.query(Task05).all()
        assert len(task05) == 5
