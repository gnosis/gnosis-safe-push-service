import json

from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from gnosis_safe_push_service.ether.tests.factories import \
    get_eth_address_with_key

from ..models import Device, DevicePair
from .factories import get_signature_json

faker = Faker()


class TestViews(APITestCase):

    def test_auth_creation(self):
        eth_account, eth_key = get_eth_address_with_key()
        push_token = faker.name()
        signature = get_signature_json(push_token, eth_key)
        auth_data = {
            'pushToken': push_token,
            'signature': signature
        }

        request = self.client.post(reverse('api:auth-creation'), data=json.dumps(auth_data),
                                   content_type='application/json')
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Device.objects.get(owner=eth_account).push_token, push_token)

    def test_auth_fail(self):
        request = self.client.post(reverse('api:auth-creation'), data=json.dumps({}),
                                   content_type='application/json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pairing_creation(self):
        chrome_address, chrome_key = get_eth_address_with_key()
        device_address, device_key = get_eth_address_with_key()

        expiration_date = timezone.now().isoformat()
        connection_type = 'mobile'

        data = {
            "temporary_authorization": {
                "expiration_date": expiration_date,
                "connection_type": connection_type,
                "signature": get_signature_json(expiration_date + connection_type, chrome_key),
            },
            "signature": get_signature_json(chrome_address, device_key)
        }

        Device.objects.create(push_token=faker.name(), owner=chrome_address)
        Device.objects.create(push_token=faker.name(), owner=device_address)

        request = self.client.post(reverse('api:pairing-creation'),
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)

        self.assertEquals(DevicePair.objects.count(), 2)