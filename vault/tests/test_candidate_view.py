from django.test import TestCase, Client
from django.urls import reverse
from vault.models.candidate import Candidate
from django.core.files.uploadedfile import SimpleUploadedFile

class CandidateViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        cls.candidate = Candidate.objects.create(
            full_name='John Doe',
            email='john.doe@example.com', 
            date_of_birth='1990-01-01',
            years_of_experience=5,
            department_id=1,
            resume=SimpleUploadedFile('test_resume.pdf', content=b'test', content_type='application/pdf')
        )

    def test_register_candidate(self):
        response = self.client.post(reverse('register_candidate'), {
            'full_name': 'Jane Doe',
            'email': 'jane.doe@example.com',
            'date_of_birth': '1995-02-15',
            'years_of_experience': 3,
            'department_id': 1,
            'resume': SimpleUploadedFile('test_resume.pdf', content=b'test', content_type='application/pdf')
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Candidate.objects.last().full_name, 'Jane Doe')
        self.assertEqual(Candidate.objects.last().email, 'jane.doe@example.com')
        self.assertEqual(Candidate.objects.last().date_of_birth.__str__(), '1995-02-15')
        self.assertEqual(Candidate.objects.last().years_of_experience, 3)
        self.assertEqual(Candidate.objects.last().department_id, 1)
        Candidate.objects.last().delete()

    def test_list_candidates(self):
        response = self.client.get(reverse('list_candidates'), HTTP_X_ADMIN='1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['candidates']), 1)
        self.assertEqual(response.json()['candidates'][0]['full_name'], 'John Doe')

    def test_download_resume(self):
        response = self.client.get(reverse('download_resume', args=[self.candidate.id]), HTTP_X_ADMIN='1')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        return super().tearDown()

    