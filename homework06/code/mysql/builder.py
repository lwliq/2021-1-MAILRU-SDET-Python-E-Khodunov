from mysql.models import Task01, Task02, Task03, Task04, Task05


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    def create_task01_from_dict(self, values: dict):

        task01 = Task01(
            count=values['count']
        )
        self.client.session.add(task01)
        return task01

    def create_task02_from_dict(self, values: dict):

        task02 = Task02(
            r_type=values['type'],
            count=values['count']
        )
        self.client.session.add(task02)
        return task02

    def create_task03_from_dict(self, values: dict):

        task03 = Task03(
            location=values['location'],
            count=values['count']
        )
        self.client.session.add(task03)
        return task03

    def create_task04_from_dict(self, values: dict):

        task04 = Task04(
            ip=values['ip'],
            location=values['location'],
            status=values['status'],
            size=values['size']
        )
        self.client.session.add(task04)
        return task04

    def create_task05_from_dict(self, values: dict):

        task05 = Task05(
            ip=values['ip'],
            count=values['count']
        )
        self.client.session.add(task05)
        return task05
