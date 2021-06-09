import allure
import docker
import os
from docker.models.containers import Container


def generate_myapp_config_file(config: dict, test_dir: str) -> str:
    file_path = os.path.join(test_dir, 'myapp_config.conf')
    with open(file_path, 'w') as file:
        for key in config:
            file.write(f"{key} = '{config[key]}'\n")

    return file_path


def write_to_file(data, file_path):
    with open(file_path, 'wb') as file:
        file.write(data)


class AppMockDockerClient:
    client = docker.from_env()

    def __init__(self, tag: str, label: str, test_dir: str):

        self.test_dir = test_dir
        vk_api_name = 'vk_api_' + label
        app_name = 'myapp_' + label

        env = {
            'MYSQL_USER': 'test_qa',
            'MYSQL_PASSWORD': 'qa_test',
            'MYSQL_HOST': tag + '_mysql',
            'MYSQL_PORT': '3306',
            'MYSQL_DB': label,
            'VK_API_HOST': '0.0.0.0',
            'VK_API_PORT': '80',
        }

        self.mock_container: Container = self.client.containers.run(
            name=vk_api_name,
            image=tag + '_vk_api:latest',
            environment=env,
            detach=True,
            network=tag + '_network'
        )

        myapp_config = {
            'APP_HOST': '0.0.0.0',
            'APP_PORT': '80',
            'MYSQL_HOST': tag + '_mysql',
            'MYSQL_PORT': '3306',
            'MYSQL_DB': label,
            'VK_URL': f'{vk_api_name}:80'
        }

        self.myapp_config_file = generate_myapp_config_file(myapp_config, test_dir)

        with open(self.myapp_config_file, 'r') as file:
            allure.attach(file.read(), 'myapp.conf',
                          attachment_type=allure.attachment_type.TEXT)

        self.app_container: Container = self.client.containers.run(
            name=app_name,
            command=f'/app/myapp --config={self.myapp_config_file}',
            image='myapp:latest',
            volumes_from=[os.getenv('HOSTNAME')],
            detach=True,
            network=tag + '_network'
        )

    def save_logs(self):
        file_path = os.path.join(self.test_dir, 'app_docker.log')
        write_to_file(self.app_container.logs(), file_path)
        allure.attach(self.app_container.logs().decode('utf-8'), 'myapp_docker.log',
                      attachment_type=allure.attachment_type.TEXT)
        file_path = os.path.join(self.test_dir, 'mock_docker.log')
        write_to_file(self.mock_container.logs(), file_path)
        allure.attach(self.app_container.logs().decode('utf-8'), 'mock_docker.log',
                      attachment_type=allure.attachment_type.TEXT)

    def shutdown(self):
        self.save_logs()
        self.app_container.remove(v=True, force=True)
        self.mock_container.remove(v=True, force=True)
