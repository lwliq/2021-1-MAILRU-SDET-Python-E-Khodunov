from datetime import datetime

from mysql.models import User, VKUser
from faker import Faker


class MySQLBuilder:

    def __init__(self, client, faker):
        self.client = client
        self.faker: Faker = faker

    def create_fake_user(self, access=True, active=False, vk=False):

        user = User(
            username=self.faker.user_name()[:16],
            password=self.faker.password()[:255],
            email=self.faker.email()[:64],
            access=int(access),
            active=int(active),
            start_active_time=None
        )

        self.client.add(user)

        if vk:
            vk_user = self.create_vk_user(user.username)
            self.client.add(vk_user)

            return user, vk_user

        return user

    def create_vk_user(self, username, vk_id=None):

        if vk_id is None:
            vk_id = self.faker.random.randint(0, 32767)

        vk_user = VKUser(
            username=username,
            vk_id=str(vk_id)
        )

        self.client.add(vk_user)
        return vk_user


