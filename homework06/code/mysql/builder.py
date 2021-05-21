from mysql.models import RequestsCount, RequestsCountByType, Top10MostFrequentLocations, Top5LocationsBySize,\
    Top5MostFrequentIps


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    def create_requests_count(self, values: dict):

        task01 = RequestsCount(
            count=values['count']
        )
        self.client.session.add(task01)
        return task01

    def create_requests_count_by_type(self, values: dict):

        task02 = RequestsCountByType(
            r_type=values['type'],
            count=values['count']
        )
        self.client.session.add(task02)
        return task02

    def create_top_10_most_frequent_locations(self, values: dict):

        task03 = Top10MostFrequentLocations(
            location=values['location'],
            count=values['count']
        )
        self.client.session.add(task03)
        return task03

    def create_top_5_locations_by_size(self, values: dict):

        task04 = Top5LocationsBySize(
            ip=values['ip'],
            location=values['location'],
            status=values['status'],
            size=values['size']
        )
        self.client.session.add(task04)
        return task04

    def create_top_5_most_frequent_ips(self, values: dict):

        task05 = Top5MostFrequentIps(
            ip=values['ip'],
            count=values['count']
        )
        self.client.session.add(task05)
        return task05
