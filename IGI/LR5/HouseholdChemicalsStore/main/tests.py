from django.test import TestCase, Client as DjangoClient
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import ReviewForm
from .models import *

class ViewTests(TestCase):
    def setUp(self):
        self.django_client = DjangoClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client_user = Client.objects.create(user=self.user, phone='1234567890', email='test@example.com', date_of_birth='2000-01-01', city='Минск')
        self.about_company = about_company.objects.create(content='Lorem ipsum dolor sit amet, consectetur adipiscing elit.')

    def test_home_view(self):
        self.django_client.login(username='testuser', password='password')
        response = self.django_client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_about_company_view(self):
        response = self.django_client.get(reverse('about_company'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_company.html')

    def test_contacts_view(self):
        response = self.django_client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts.html')

    def test_faq_view(self):
        response = self.django_client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq.html')

    def test_news_view(self):
        response = self.django_client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news.html')

    def test_privacy_policy_view(self):
        response = self.django_client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'privacy_policy.html')

    def test_promo_coupons_view(self):
        response = self.django_client.get(reverse('promo_coupons'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'promo_coupons.html')

    def test_reviews_view(self):
        response = self.django_client.get(reverse('reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews.html')

    def test_vacancies_view(self):
        response = self.django_client.get(reverse('vacancies'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vacancies.html')

    def test_signup_view(self):
        response = self.django_client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_employee_signup_view(self):
        response = self.django_client.get(reverse('signup_employee'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup_employee.html')

    def test_add_review_view(self):
        self.django_client.login(username='testuser', password='password')
        response = self.django_client.get(reverse('add_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_review.html')
        # Проверяем, что форма, используемая на странице, действительно является формой ReviewForm
        self.assertIsInstance(response.context['form'], ReviewForm)

    def test_signup_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.django_client.post(reverse('signup'), form_data)
        self.assertEqual(response.status_code, 200)

    def test_order_create_view(self):
        self.django_client.login(username='testuser', password='password')
        response = self.django_client.get(reverse('order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_create.html')

    def test_order_create_form_valid(self):
        form_data = {
            'client': self.client_user.pk,
            'sale_date': '2024-05-28',
            'delivery_date': '2024-06-04',
            'total_price': 100,
        }
        response = self.django_client.post(reverse('order_create'), form_data)
        self.assertEqual(response.status_code, 200)