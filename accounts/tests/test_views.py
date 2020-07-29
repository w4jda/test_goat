from django.test import TestCase
from accounts.models import Token
from unittest.mock import patch

import accounts.views

class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'})
        self.assertRedirects(response, '/')

    def test_creates_a_token_associated_with_email(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'})

        token = Token.objects.first()
        self.assertEqual(token.email, 'edith@example.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token(self, mock_send_mail):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'})

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

    @patch('accounts.views.send_mail')
    def test_sends_emails_to_address_from_post(self, mock_send_mail):
        
        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs =mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['edith@example.com'])

    def test_adds_success_message(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        }, follow=True)  # To look what's "behind" 302

        message = list(response.context['messages'])[0]
        self.assertEqual(message.message,
                         "Check your email, we've sent you a link you can use to log in."
                         )
        self.assertEqual(message.tags, "success")


class LoginViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')
