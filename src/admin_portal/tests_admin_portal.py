from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from in_brief.models import Article, Category
from apps.intake.models import Lead
from admin_portal.models import SystemSettings

class AdminPortalTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(username='admin', password='password', email='admin@test.com')
        self.client.login(username='admin', password='password')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.article = Article.objects.create(
            title='Test Article',
            slug='test-article',
            content='Test Content',
            author=self.user,
            is_published=True
        )
        self.article.categories.add(self.category)
        self.lead = Lead.objects.create(
            full_name='Test Lead',
            contact_info='test@test.com',
            case_type='OTHER',
            source='Google',
            location='São Paulo'
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('admin_portal:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_articles', response.context)
        self.assertIn('leads_by_source', response.context)
        self.assertIn('leads_by_location', response.context)

    def test_article_list(self):
        response = self.client.get(reverse('admin_portal:article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Article')

    def test_category_list(self):
        response = self.client.get(reverse('admin_portal:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')

    def test_settings_view(self):
        response = self.client.get(reverse('admin_portal:settings_general'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('settings', response.context)
