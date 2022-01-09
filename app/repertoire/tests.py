from io import StringIO
import json

from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from repertoire.serializers import (
    Contributor, 
    File, 
    Work
)


class FileTestCase(APITestCase):
    expected_response = dict()

    def setUp(self):
        self.file_1 = File.objects.create(
            filename = "sony.csv",
            work_count = 2
        )
        self.file_2 = File.objects.create(
            filename = "universal.csv",
            work_count = 1
        )
        self.file_3 = File.objects.create(
            filename = "warner.csv",
            work_count = 3
        )

        self.expected_response['files'] = [
            {'id': self.file_1.id, 'filename': 'sony.csv', 'work_count': 2},
            {'id': self.file_2.id, 'filename': 'universal.csv', 'work_count': 1}, 
            {'id': self.file_3.id, 'filename': 'warner.csv', 'work_count': 3}
        ]

        self.expected_response['file_1_response'] = self.expected_response['files'][0]
        self.expected_response['file_2_response'] = self.expected_response['files'][1]
        self.expected_response['file_3_response'] = self.expected_response['files'][2]

        self.expected_response['not_found'] = {
            "detail": "Not found."
        }


    def test_list_files(self):
        response = self.client.get("/files/")
        
        expected_response = self.expected_response['files']
        request_response = json.loads(response.content)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            request_response,
            expected_response
        )

        
    def test_get_file_1_ok(self):
        response = self.client.get(f"/files/{self.file_1.id}/")
        
        expected_response = self.expected_response['file_1_response']
        request_response = json.loads(response.content)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            request_response,
            expected_response
        )


    def test_get_file_2_ok(self):
        response = self.client.get(f"/files/{self.file_2.id}/")
        
        expected_response = self.expected_response['file_2_response']
        request_response = json.loads(response.content)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            request_response,
            expected_response
        )


    def test_get_file_3_ok(self):
        response = self.client.get(f"/files/{self.file_3.id}/")
        
        expected_response = self.expected_response['file_3_response']
        request_response = json.loads(response.content)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            request_response,
            expected_response
        )


    def test_get_file_not_found(self):
        response = self.client.get(f"/files/4/")
        
        expected_response = self.expected_response['not_found']
        request_response = json.loads(response.content)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            request_response,
            expected_response
        )


class ContributorTestCase(APITestCase):
    expected_response = dict()

    def create_contributor(self, name):
        return Contributor.objects.create(
            name = name,
        )

    def setUp(self):
        self.contributor_1 = self.create_contributor(
            name = "Edward Christopher Sheeran",
        )
        self.contributor_2 = self.create_contributor(
            name = "Obispo Pascal Michel",
        )

        self.contributor_3 = self.create_contributor(
            name = "Florence Lionel Jacques",
        )

    def test_contributor_creation(self):
        obj = self.create_contributor(
            name="test"
        )
        self.assertTrue(isinstance(obj, Contributor))
        self.assertEqual(obj.__str__(), obj.name)

    def test_contributors_with_same_name(self):
        with self.assertRaises(Exception) as raised:
            self.contributor_1 = self.create_contributor(
                name = "Edward Christopher Sheeran",
                )
        self.assertEqual(IntegrityError, type(raised.exception))

