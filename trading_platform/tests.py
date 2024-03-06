# from rest_framework import status
# from rest_framework.test import APITestCase
#
# from trading_platform.models import Product
# from user.models import User
#
#
# class NetworkNodeTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='test@example.com',
#             password='testpassword'
#         )
#         self.user.is_superuser = True
#         self.user.is_active = True
#         self.user.is_staff = True
#         self.user.save()
#
#         self.client.force_authenticate(self.user)
#
#         product = Product.objects.create(
#             name='product_1',
#             model='product_1',
#             release_date='2023-09-10'
#         )
#
#     def test_create_network_node(self):
#         product = Product.objects.create(
#             name='product_1',
#             model='product_1',
#             date_release='2023-09-10'
#         )
#
#         data = {
#             "name": "Транзисторный завод",
#             "email": "email1@example.com",
#             "city": "Город первого звена",
#             "street": "Улица первого звена",
#             "house_number": "1",
#             "node_type": "Factory",
#             "product_ids": [product.pk],
#             "debt": 0.00
#         }
#
#         response = self.client.post('/platform/network-node/', data=data)
#
#         self.assertEqual(
#             response.status_code,
#             status.HTTP_201_CREATED
#         )
#         self.assertEqual(
#             response.json(),
#             {
#                 "id": response.json()["id"],
#                 "name": "Транзисторный завод",
#                 "email": "email1@example.com",
#                 "city": "Город первого звена",
#                 "street": "Улица первого звена",
#                 "house_number": "1",
#                 "node_type": "Factory",
#                 "supplier": "null",
#                 "products": [
#                     {
#                         "id": 1,
#                         "name": "Транзистор",
#                         "model": "Модель продукта",
#                         "release_date": '2023-09-10',
#                         "created_at": response.json()['products']["created_at"]
#                     }
#                 ],
#                 "debt": "0.00",
#                 "created_at": response.json()["created_at"],
#                 "level": 0
#             },
#         )
import pprint

from django.test import TestCase, Client
from rest_framework import status

from trading_platform.models import Product
from user.models import User


class NetworkNodeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword'
        )
        self.user.is_superuser = True
        self.user.is_active = True
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)

        self.product = Product.objects.create(
            name='product_1',
            model='product_1',
            release_date='2023-09-10'
        )

    def test_create_network_node(self):
        data = {
            "name": "Транзисторный завод",
            "email": "email1@example.com",
            "city": "Город первого звена",
            "street": "Улица первого звена",
            "house_number": "1",
            "node_type": "Factory",
            "product_ids": [self.product.pk],
            "debt": 0.00
        }

        response = self.client.post('/platform/network-node/', data=data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_json = {
            "id": response.json()["id"],
            "name": "Транзисторный завод",
            "email": "email1@example.com",
            "city": "Город первого звена",
            "street": "Улица первого звена",
            "house_number": "1",
            "node_type": "Factory",
            "supplier": None,
            "products": [
                {
                    "id": self.product.pk,
                    "name": "product_1",
                    "model": "product_1",
                    "release_date": '2023-09-10',
                    "created_at": response.json()['products'][0]["created_at"]
                }
            ],
            "debt": "0.00",
            "created_at": response.json()["created_at"],
            "level": 0
        }

        self.assertJSONEqual(response.content, expected_json)

    def test_update_network_node(self):
        data_before = {
            "name": "Транзисторный завод",
            "email": "email1@example.com",
            "city": "Город первого звена",
            "street": "Улица первого звена",
            "house_number": "1",
            "node_type": "Factory",
            "product_ids": [self.product.pk],
            "debt": 0.00
        }

        post_response = self.client.post('/platform/network-node/', data=data_before, content_type='application/json')

        data_after = {
            "name": "NewТранзисторный завод",
            "email": "Newemail1@example.com",
            "city": "NewГород первого звена",
            "street": "NewУлица первого звена",
            "house_number": "1",
            "node_type": "Factory",
            "product_ids": [self.product.pk],
            "debt": 1.00
        }

        put_response = self.client.put(f'/platform/network-node/{post_response.json()["id"]}/', data=data_after,
                                       content_type='application/json')

        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        expected_json = {
            "id": put_response.json()["id"],
            "name": "NewТранзисторный завод",
            "email": "Newemail1@example.com",
            "city": "NewГород первого звена",
            "street": "NewУлица первого звена",
            "house_number": "1",
            "node_type": "Factory",
            "supplier": None,
            "products": [
                {
                    "id": self.product.pk,
                    "name": "product_1",
                    "model": "product_1",
                    "release_date": '2023-09-10',
                    "created_at": put_response.json()['products'][0]["created_at"]
                }
            ],
            "debt": "0.00",
            "created_at": put_response.json()["created_at"],
            "level": 0
        }

        self.assertJSONEqual(put_response.content, expected_json)

    def test_delete_network_node(self):
        data = {
            "name": "Транзисторный завод",
            "email": "email1@example.com",
            "city": "Город первого звена",
            "street": "Улица первого звена",
            "house_number": "1",
            "node_type": "Factory",
            "product_ids": [self.product.pk],
            "debt": 0.00
        }

        post_response = self.client.post('/platform/network-node/', data=data, content_type='application/json')
        del_response = self.client.delete(f'/platform/network-node/{post_response.json()["id"]}/')

        self.assertEqual(
            del_response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_get_network_node(self):
        data = {
            "name": "Транзисторный завод",
            "email": "email1@example.com",
            "city": "Город первого звена",
            "street": "Улица первого звена",
            "house_number": "1",
            "node_type": "Factory",
            "product_ids": [self.product.pk],
            "debt": 0.00
        }

        post_response = self.client.post('/platform/network-node/', data=data, content_type='application/json')
        get_response = self.client.get(f'/platform/network-node/{post_response.json()["id"]}/')

        self.assertEqual(
            get_response.status_code,
            status.HTTP_200_OK
        )

        expected_json = {
            "id": post_response.json()["id"],
            "name": "Транзисторный завод",
            "email": "email1@example.com",
            "city": "Город первого звена",
            "street": "Улица первого звена",
            "house_number": "1",
            "node_type": "Factory",
            "supplier": None,
            "products": [
                {
                    "id": self.product.pk,
                    "name": "product_1",
                    "model": "product_1",
                    "release_date": '2023-09-10',
                    "created_at": post_response.json()['products'][0]["created_at"]
                }
            ],
            "debt": "0.00",
            "created_at": post_response.json()["created_at"],
            "level": 0
        }

        self.assertJSONEqual(get_response.content, expected_json)

    def test_list_network_node(self):
        data_1 = {
            "name": "Транзисторный завод",
            "email": "email1@example.com",
            "city": "Город первого звена",
            "street": "Улица первого звена",
            "house_number": "1",
            "node_type": "Factory",
            "product_ids": [self.product.pk],
            "debt": 0.00
        }

        data_2 = {
            "name": "Коминтерновский завод",
            "email": "email1@example.com",
            "city": "Город первого звена",
            "street": "Улица первого звена",
            "house_number": "1",
            "node_type": "Factory",
            "product_ids": [self.product.pk],
            "debt": 0.00
        }

        self.client.post('/platform/network-node/', data=data_1, content_type='application/json')
        self.client.post('/platform/network-node/', data=data_2, content_type='application/json')

        get_response = self.client.get('/platform/network-node/')

        self.assertEqual(
            get_response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(len(get_response.json()), 2)
