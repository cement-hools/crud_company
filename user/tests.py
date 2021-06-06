from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.models import Company, News
from api.serializers import (CompanySerializer, NewsSerializer,
                             ProfileSerializer)
from .models import User, Profile, Roles


class CompanyApiTestCase(APITestCase):
    def setUp(self):
        self.user_admin = User.objects.create_superuser(username='admin')
        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')

        self.company_1 = Company.objects.create(
            name='company_1',
            description='test company_1'
        )
        self.company_2 = Company.objects.create(
            name='company_2',
            description='test company_2'
        )

        self.profile_1 = Profile.objects.create(
            user=self.user_1, company=self.company_1
        )
        self.profile_2 = Profile.objects.create(
            user=self.user_2, company=self.company_1
        )

        self.news_1 = News.objects.create(
            author=self.user_1,
            company=self.company_1,
            title='Test news',
            text='Test text'
        )
        self.news_2 = News.objects.create(
            author=self.user_2,
            company=self.company_1,
            title='Test news',
            text='Test text'
        )

        self.client_admin = self.client_class()
        self.client_not_auth = self.client_class()

        self.client_admin.force_authenticate(self.user_admin)
        self.client.force_authenticate(self.user_1)

    def test_registration(self):
        """Регистрация пользователя."""
        self.assertEqual(3, User.objects.all().count())
        url = reverse('registration')
        username = 'user_created'

        data = {'username': username, 'password': '12qw$tuAS'}
        response = self.client_not_auth.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, User.objects.all().count())
        new_user = User.objects.all().last()
        self.assertEqual(username, new_user.username)

    def test_get_company_list(self):
        """Список всех компаний."""
        url = reverse('companies-list')
        companies = Company.objects.all()
        response = self.client.get(url)
        serializer_data = CompanySerializer(companies, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_company_detail_not_auth(self):
        """Просмотр компании неавторизованным пользователем."""
        url = reverse('companies-detail', args=(self.company_1.id,))
        response = self.client_not_auth.get(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_company_detail_owner(self):
        """Просмотр своей компании пользователем."""
        url = reverse('companies-detail', args=(self.company_1.id,))
        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.company_1.name, response.data['name'])
        self.assertEqual(2, response.data.get('amount_of_employees'))

    def test_get_company_detail_not_owner(self):
        """Просмотр не своей компании пользователем."""
        url = reverse('companies-detail', args=(self.company_2.id,))
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_new_company(self):
        """Создание админом новой компании."""
        self.assertEqual(2, Company.objects.all().count())
        data = {'name': 'company_3', 'description': 'test company_3'}
        url = reverse('companies-list')

        response = self.client_admin.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Company.objects.all().count())
        new_company = Company.objects.all().last()
        serializer_data = CompanySerializer(new_company).data

        self.assertEqual(response.data, serializer_data)

    def test_create_new_company_non_admin(self):
        """Создание не админом новой компании."""
        self.assertEqual(2, Company.objects.all().count())
        data = {'name': 'company_3', 'description': 'test company_3'}
        url = reverse('companies-list')

        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_update_company_admin(self):
        """Администратор редактирует компанию."""
        old_company = {
            'name': self.company_1.name,
            'description': self.company_1.description,
        }
        url = reverse('companies-detail', args=(self.company_1.id,))
        data = {
            'name': 'Whooosh',
            'description': 'Update',
        }
        response = self.client_admin.put(url, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.company_1.refresh_from_db()
        self.assertNotEqual(old_company['name'], self.company_1.name)
        self.assertNotEqual(old_company['description'],
                            self.company_1.description)
        self.assertEqual('Whooosh', self.company_1.name)
        self.assertEqual('Update', self.company_1.description)

    def test_update_company_employee(self):
        """Сотрудник редактирует компанию."""
        old_company = {
            'name': self.company_1.name,
            'description': self.company_1.description,
        }
        url = reverse('companies-detail', args=(self.company_1.id,))
        data = {
            'name': 'Whooosh',
            'description': 'Update',
        }
        response = self.client.put(url, data=data)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_update_company_employee_moderator(self):
        """Модератор редактирует свою компанию."""
        old_company = {
            'name': self.company_1.name,
            'description': self.company_1.description,
        }
        url = reverse('companies-detail', args=(self.company_1.id,))
        data = {
            'name': 'Whooosh',
            'description': 'Update',
        }
        self.profile_1.role = Roles.MODERATOR

        response = self.client.put(url, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.company_1.refresh_from_db()
        self.assertNotEqual(old_company['name'], self.company_1.name)
        self.assertNotEqual(old_company['description'],
                            self.company_1.description)
        self.assertEqual('Whooosh', self.company_1.name)
        self.assertEqual('Update', self.company_1.description)

    def test_get_company_list(self):
        """Список всех новостей компании."""
        url = reverse('news-list', args=(self.company_1.id,))
        news = self.company_1.news.all()
        response = self.client.get(url)
        serializer_data = NewsSerializer(news, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_news_list_not_owner(self):
        """Список всех новостей не своей компании."""
        url = reverse('news-list', args=(self.company_2.id,))
        news = self.company_2.news.all()
        response = self.client.get(url)
        serializer_data = NewsSerializer(news, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_news_detail(self):
        """Просмотр новости своей компании."""
        url = reverse('news-detail', args=(self.company_1.id, self.news_1.id,))
        response = self.client.get(url)
        serializer_data = NewsSerializer(self.news_1).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_news_detail_not_owner(self):
        """Просмотр новости не своей компании."""
        self.news_3 = News.objects.create(
            author=self.user_2,
            company=self.company_2,
            title='Test news',
            text='Test text'
        )
        url = reverse('news-detail', args=(self.company_2.id, self.news_3.id,))
        response = self.client.get(url)
        serializer_data = NewsSerializer(self.news_3).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_news_edit_author(self):
        """Автор редактирует свою новость."""
        old_news = {'title': self.news_1.title, 'text': self.news_1.text}
        url = reverse('news-detail', args=(self.company_1.id, self.news_1.id,))

        data = {'title': 'edit', 'text': 'edited text'}
        response = self.client.put(url, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.news_1.refresh_from_db()
        self.assertNotEqual(old_news['title'], self.news_1.title)
        self.assertNotEqual(old_news['text'], self.news_1.text)
        self.assertEqual('edit', self.news_1.title)
        self.assertEqual('edited text', self.news_1.text)

    def test_news_edit_non_author(self):
        """Не автор редактирует новость."""
        url = reverse('news-detail', args=(self.company_1.id, self.news_2.id,))

        data = {'title': 'edit', 'text': 'edited text'}
        response = self.client.put(url, data=data)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_news_edit_admin(self):
        """Админ редактирует новость."""
        old_news = {'title': self.news_1.title, 'text': self.news_1.text}
        url = reverse('news-detail', args=(self.company_1.id, self.news_1.id,))

        data = {'title': 'edit', 'text': 'edited text'}
        response = self.client_admin.put(url, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.news_1.refresh_from_db()
        self.assertNotEqual(old_news['title'], self.news_1.title)
        self.assertNotEqual(old_news['text'], self.news_1.text)
        self.assertEqual('edit', self.news_1.title)
        self.assertEqual('edited text', self.news_1.text)

    def test_news_edit_moderator(self):
        """Модератор редактирует новость."""
        old_news = {'title': self.news_2.title, 'text': self.news_2.text}
        url = reverse('news-detail', args=(self.company_1.id, self.news_2.id,))

        self.profile_1.role = Roles.MODERATOR

        data = {'title': 'edit', 'text': 'edited text'}
        response = self.client.put(url, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.news_2.refresh_from_db()
        self.assertNotEqual(old_news['title'], self.news_2.title)
        self.assertNotEqual(old_news['text'], self.news_2.text)
        self.assertEqual('edit', self.news_2.title)
        self.assertEqual('edited text', self.news_2.text)

    def test_news_edit_moderator_not_owner_company(self):
        """Модератор редактирует новость не своей компании."""
        old_news = {'title': self.news_2.title, 'text': self.news_2.text}
        url = reverse('news-detail', args=(self.company_2.id, self.news_2.id,))

        self.profile_1.role = Roles.MODERATOR

        data = {'title': 'edit', 'text': 'edited text'}
        response = self.client.put(url, data=data)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_new_news_in_owner_company(self):
        """Создание пользователем новой новости в своей компании."""
        self.assertEqual(2, News.objects.all().count())
        data = {'title': 'news_3', 'text': 'edited text news_3'}
        url = reverse('news-list', args=(self.company_1.id,))

        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, News.objects.all().count())
        new_news = News.objects.all().first()
        serializer_data = NewsSerializer(new_news).data

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(self.user_1, new_news.author)

    def test_create_new_news_in_not_owner_company(self):
        """Создание пользователем новой новости не в своей компании."""
        self.assertEqual(2, News.objects.all().count())
        data = {'title': 'news_3', 'text': 'edited text news_3'}
        url = reverse('news-list', args=(self.company_2.id,))

        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, News.objects.all().count())

    def test_profile_list_not_admin(self):
        """Не админ не может просматривать профили"""
        url = reverse('profiles-list')

        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        response = self.client_not_auth.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_profile_list(self):
        """Список всех профилей."""
        url = reverse('profiles-list')
        profiles = Profile.objects.all()
        response = self.client_admin.get(url)
        serializer_data = ProfileSerializer(profiles, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
