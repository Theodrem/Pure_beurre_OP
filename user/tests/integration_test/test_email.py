from django.test import TestCase
from django.core import mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User


class EmailTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="user_test",
                                 password="Salut_test_pass",
                                 email="theotim@outlook.fr")
        self.user = User.objects.get(username="user_test")

    def test_send_email_get(self):
        # First we get the initial password reset form.
        response = self.client.get(reverse('reset_password'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['user/reset_password.html'])

    def test_send_email_post(self):
        #  Post the response with our "email address"
        response = self.client.post(reverse('reset_password'), {'email': 'theotim@outlook.fr'})
        self.assertEqual(response.status_code, 302)
        # At this point the system will "send" us an email. We can "check" it thusly:
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Réinitialisation du mot de passe sur testserver')

        #Generate uid and token
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        #Use the token to get the password change form
        response = self.client.get(reverse('password_reset_confirm', args=[uid, token]))
        #redirect to /reset/Mg/set-password

        self.assertEqual(response.status_code, 302)

        # We post to the same url with our new password:
        form = {'new_password1': 'pologne102', 'new_password2': 'pologne102'}
        response = self.client.post(response.url, form)
        # redirect to /reset_password_complete/
        self.assertEqual(response.status_code, 302)

        #check connexion user with new password
        self.client.login(username="user_test", password="pologne102")
        self.assertIn('_auth_user_id', self.client.session)


