from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Recipient

User = get_user_model()


class RecipientTest(TestCase):

    def test_create_recipient(self):

        user = User.objects.create_user(email="test@test.com", password="12345")

        recipient = Recipient.objects.create(
            email="client@test.com", full_name="Ivan Ivanov", owner=user
        )

        self.assertEqual(recipient.owner, user)
