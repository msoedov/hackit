import factory
from faker import Factory as FakerFactory

from ..models import File, User

faker = FakerFactory.create()


class UserFactory(factory.Factory):
    username = factory.LazyAttribute(lambda o: faker.user_name())
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.username)

    class Meta:
        model = User


class FileFactory(factory.Factory):
    name = 'kitty.jpeg'

    class Meta:
        model = File
