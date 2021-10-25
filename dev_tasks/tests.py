from uuid import uuid4

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Developer, Task, Team


class DeveloperModelTests(TestCase):
    def test_sanity(self):
        self.client.post(reverse('dev_tasks:task_create'), {'type': 'A', 'points': 5}, 'application/json')
        task = Task.objects.order_by('-id').get()
        self.assertIsNone(task.assigned)
        team_id = None
        for _ in range(3):
            unique = uuid4()
            self.client.post(reverse('dev_tasks:developer_create'), {
                'MainBranch': 'pro',
                'WebframeHaveWorkedWith': 'vue',
                'LanguageHaveWorkedWith': 'php',
                'SOPartFreq': unique
            }, 'application/json')
            dev_team_id = Developer.objects.filter(SOPartFreq=unique).values('team_id')[0]['team_id']
            self.assertEqual(team_id, dev_team_id) if team_id is not None else True
            team_id = dev_team_id
            self.assertIsNotNone(dev_team_id)
        task.refresh_from_db()
        self.assertEqual(task.assigned.replace(tzinfo=None, microsecond=0), timezone.now().replace(tzinfo=None, microsecond=0))

    def test_example_1(self):
        for _ in range(2):  # 2 fullstack
            self.client.post(reverse('dev_tasks:developer_create'), {
                'MainBranch': 'pro', 'WebframeHaveWorkedWith': 'vue', 'LanguageHaveWorkedWith': 'php'
            }, 'application/json')
        for _ in range(3):  # and 3 academic developers enter the system
            self.client.post(reverse('dev_tasks:developer_create'), {
                'MainBranch': 'pro', 'EdLevel': 'ba'
            }, 'application/json')
        unique = uuid4()
        self.client.post(reverse('dev_tasks:developer_create'), {
            'MainBranch': 'pro', 'WebframeHaveWorkedWith': 'vue', 'LanguageHaveWorkedWith': 'php', 'SOPartFreq': unique
        }, 'application/json')  # when the next full stack developer is added
        dev_team_id = Developer.objects.filter(SOPartFreq=unique).values('team_id')[0]['team_id']
        team = Team.objects.get(id=dev_team_id)
        self.assertEqual(team.team_type, 1)  # the incomplete T1 team takes precedence over the incomplete T3 team

    def test_example_2(self):
        # 1 type A is added
        self.client.post(reverse('dev_tasks:task_create'), {'type': 'A', 'points': 5}, 'application/json')
        for _ in range(2):  # 2 full stack developers are added to the system
            self.client.post(reverse('dev_tasks:developer_create'), {
                'MainBranch': 'pro', 'WebframeHaveWorkedWith': 'vue', 'LanguageHaveWorkedWith': 'php'
            }, 'application/json')
        # 1 type D task is added
        self.client.post(reverse('dev_tasks:task_create'), {'type': 'D', 'points': 1}, 'application/json')
        # 2 academic, 2 backend, and 2 front end are added
        unique = None
        for _ in range(2):  # 2 full stack developers are added to the system
            self.client.post(reverse('dev_tasks:developer_create'), {
                'MainBranch': 'pro', 'WebframeHaveWorkedWith': 'vue'
            }, 'application/json')
            self.client.post(reverse('dev_tasks:developer_create'), {
                'MainBranch': 'pro', 'LanguageHaveWorkedWith': 'php'
            }, 'application/json')
            unique = uuid4()
            self.client.post(reverse('dev_tasks:developer_create'), {
                'MainBranch': 'pro', 'EdLevel': 'ba', 'SOPartFreq': unique
            }, 'application/json')
        dev_team_id = Developer.objects.filter(SOPartFreq=unique).values('team_id')[0]['team_id']
        team_from_dev = Team.objects.get(id=dev_team_id)
        self.assertEqual(team_from_dev.team_type, 4)  # T4 team is created
        task_d = Task.objects.filter(type='D')
        self.assertEqual(len(task_d), 1)  # Making sure that only one task of type D exists
        # type D task is assigned
        self.assertEqual(task_d[0].assigned.replace(tzinfo=None, microsecond=0), timezone.now().replace(tzinfo=None, microsecond=0))
        self.client.post(reverse('dev_tasks:developer_create'), {
            'MainBranch': 'pro', 'WebframeHaveWorkedWith': 'vue', 'LanguageHaveWorkedWith': 'php'
        }, 'application/json')  # 1 full stack is added
        task_a = Task.objects.filter(type='A')
        self.assertEqual(len(task_a), 1)
        # the type A task is assigned
        self.assertEqual(task_a[0].assigned.replace(tzinfo=None, microsecond=0), timezone.now().replace(tzinfo=None, microsecond=0))

    def test_is_pro(self):
        dev = Developer(MainBranch='I am a student who is learning to code')
        self.assertFalse(dev.is_pro())
        dev = Developer(MainBranch='I am a developer by profession')
        self.assertTrue(dev.is_pro())
        dev = Developer(MainBranch='I am a student who is learning to code. Definitely not a pro.')
        self.assertFalse(dev.is_pro())
        dev = Developer(MainBranch='')
        self.assertFalse(dev.is_pro())
        dev = Developer()
        self.assertFalse(dev.is_pro())

    def test_is_front(self):
        dev = Developer(WebframeHaveWorkedWith='Laravel;Symfony')
        self.assertFalse(dev.is_front())
        dev = Developer(WebframeHaveWorkedWith='Angular;Flask;Vue.js')
        self.assertTrue(dev.is_front())
        dev = Developer(WebframeHaveWorkedWith='VUE')
        self.assertTrue(dev.is_front())
        dev = Developer(WebframeHaveWorkedWith='')
        self.assertFalse(dev.is_front())
        dev = Developer()
        self.assertFalse(dev.is_front())

    def test_is_back(self):
        dev = Developer(LanguageHaveWorkedWith='JavaScript;Python')
        self.assertTrue(dev.is_back())
        dev = Developer(LanguageHaveWorkedWith='C++;HTML/CSS;JavaScript;Objective-C;PHP;Swift')
        self.assertTrue(dev.is_back())
        dev = Developer(LanguageHaveWorkedWith='Objective-C')
        self.assertFalse(dev.is_back())
        dev = Developer(LanguageHaveWorkedWith='JavaScript')
        self.assertFalse(dev.is_back())
        dev = Developer(LanguageHaveWorkedWith='')
        self.assertFalse(dev.is_back())
        dev = Developer()
        self.assertFalse(dev.is_back())

    def test_is_full(self):
        dev = Developer(LanguageHaveWorkedWith='JavaScript;Python', WebframeHaveWorkedWith='Angular')
        self.assertTrue(dev.is_full())
        dev = Developer(LanguageHaveWorkedWith='JavaScript;Python', WebframeHaveWorkedWith='Laravel')
        self.assertFalse(dev.is_full())
        dev = Developer(LanguageHaveWorkedWith='C++;HTML/CSS;JavaScript;Objective-C;PHP;Swift')
        self.assertFalse(dev.is_full())
        dev = Developer()
        self.assertFalse(dev.is_full())

    def test_is_academic(self):
        dev = Developer(LanguageHaveWorkedWith='JavaScript;Python', WebframeHaveWorkedWith='Angular')
        self.assertFalse(dev.is_academic())
        dev = Developer(EdLevel='High school diploma')
        self.assertFalse(dev.is_academic())
        dev = Developer(EdLevel='Professional courses')
        self.assertFalse(dev.is_academic())
        dev = Developer(EdLevel='Autodidact')
        self.assertFalse(dev.is_academic())
        dev = Developer(EdLevel='B.Sc Mathematics')
        self.assertTrue(dev.is_academic())
        dev = Developer(EdLevel='Bachelor of Arts')
        self.assertTrue(dev.is_academic())
        dev = Developer()
        self.assertFalse(dev.is_academic())
