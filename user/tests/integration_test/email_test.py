from django.test import TestCase
from django.urls import reverse
from django.core import mail

from django.contrib.auth.models import User


class EmailTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="user_test",
                                 password="password",
                                 email="email@email_bidon.fr")
        self.user = User.objects.get(username="user_test")

    def test_send_email(self):
        # Send message.
        mail.send_mail(
            'Subject here', 'Réinitialisation du mot de passe sur pure-beurre-th.herokuapp.com',
            'from@example.com', ["email@email_bidon.fr"],
            fail_silently=False,
        )

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Réinitialisation du mot de passe sur pure-beurre-th.herokuapp.com')



