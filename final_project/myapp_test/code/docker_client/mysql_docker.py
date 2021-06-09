import docker
import io
import tarfile
import os
from docker.models.containers import Container


class MySQLDockerClient:
    client = docker.from_env()

    def __init__(self, tag: str):

        env = {
            'MYSQL_ROOT_PASSWORD': 'pass',
            'MYSQL_USER': 'test_qa',
            'MYSQL_PASSWORD': 'qa_test'
        }

        self.mysql_container: Container = self.client.containers.run(
            name=tag + '_mysql',
            image='percona:latest',
            environment=env,
            detach=True,
            network=tag + '_network'
        )

    def shutdown(self):
        self.mysql_container.remove(v=True, force=True)
