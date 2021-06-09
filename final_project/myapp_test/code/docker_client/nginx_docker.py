import allure
import docker
import os
from docker.models.containers import Container


def read_template(template_path: str):
    with open(template_path, 'r') as file:
        template = file.read()

    return template


def generate_nginx_config_file(template: str, app_host: str, test_dir: str) -> str:
    config = template.format(f'http://{app_host}:80/')
    allure.attach(config, 'nginx.conf',
                  attachment_type=allure.attachment_type.TEXT)
    file_path = os.path.join(test_dir, 'nginx.conf')
    with open(file_path, 'w') as file:
        file.write(config)

    return file_path


def write_to_file(data, file_path):
    with open(file_path, 'wb') as file:
        file.write(data)


class NginxDockerClient:
    client = docker.from_env()

    def __init__(self, tag: str, label: str, test_dir: str):

        self.test_dir = test_dir
        proxy_name = 'proxy_' + label
        app_host = 'myapp_' + label

        template = read_template(os.path.join('code', 'docker_client', 'config_templates', 'nginx.conf'))
        proxy_config_file = generate_nginx_config_file(
            template=template,
            app_host=app_host,
            test_dir=self.test_dir
        )

        self.proxy_container: Container = self.client.containers.run(
            name=proxy_name,
            image='nginx:alpine',
            volumes_from=[os.getenv('HOSTNAME')],
            command=f"nginx -c {proxy_config_file} -g 'daemon off;'",
            detach=True,
            network=tag + '_network'
        )

    def save_logs(self):
        file_path = os.path.join(self.test_dir, 'proxy_docker.log')
        write_to_file(self.proxy_container.logs(), file_path)
        allure.attach(self.proxy_container.logs().decode('utf-8'), 'nginx_docker.log',
                      attachment_type=allure.attachment_type.TEXT)

    def shutdown(self):
        self.save_logs()
        self.proxy_container.remove(v=True, force=True)

