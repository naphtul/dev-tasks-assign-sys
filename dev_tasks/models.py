from django.contrib import admin
from django.db import models


class Team(models.Model):
    team_type = models.SmallIntegerField(default=1)
    full_stack_seats = models.SmallIntegerField(default=3)
    academic_seats = models.SmallIntegerField(default=3)
    frontend_seats = models.SmallIntegerField(default=3)
    backend_seats = models.SmallIntegerField(default=3)
    task_capacity = models.SmallIntegerField(default=15)

    def is_ready(self) -> bool:
        """
        Determines if a team is ready to take on tasks
        :return: True or False
        :rtype: bool
        """
        return not self.full_stack_seats and not self.academic_seats and not self.backend_seats and \
            not self.frontend_seats

    def is_eligible(self, task_type) -> bool:
        """
        Determines if a team is eligible to receive a task of the specified type.
        :param str task_type: E.g. 'A'
        :return: True or False
        :rtype: bool
        """
        eligible_task_types = {
            '1': {'A', 'B', 'C', 'D'},
            '2': {'B', 'C'},
            '3': {'A'},
            '4': {'D'},
        }
        return task_type in eligible_task_types[str(self.team_type)]


class Task(models.Model):
    type = models.CharField(max_length=1)
    points = models.SmallIntegerField()
    assigned = models.DateTimeField(default=None, null=True)
    created = models.DateTimeField(auto_now_add=True)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE, default=None, null=True)


class Developer(models.Model):
    MainBranch = models.CharField(max_length=100)
    Employment = models.CharField(max_length=100)
    Country = models.CharField(max_length=100)
    US_State = models.CharField(max_length=100)
    UK_Country = models.CharField(max_length=100)
    EdLevel = models.CharField(max_length=100)
    Age1stCode = models.CharField(max_length=100)
    LearnCode = models.CharField(max_length=100)
    YearsCode = models.CharField(max_length=100)
    YearsCodePro = models.CharField(max_length=100)
    DevType = models.CharField(max_length=100)
    OrgSize = models.CharField(max_length=100)
    Currency = models.CharField(max_length=100)
    CompTotal = models.CharField(max_length=100)
    CompFreq = models.CharField(max_length=100)
    LanguageHaveWorkedWith = models.CharField(max_length=100)
    LanguageWantToWorkWith = models.CharField(max_length=100)
    DatabaseHaveWorkedWith = models.CharField(max_length=100)
    DatabaseWantToWorkWith = models.CharField(max_length=100)
    PlatformHaveWorkedWith = models.CharField(max_length=100)
    PlatformWantToWorkWith = models.CharField(max_length=100)
    WebframeHaveWorkedWith = models.CharField(max_length=100)
    WebframeWantToWorkWith = models.CharField(max_length=100)
    MiscTechHaveWorkedWith = models.CharField(max_length=100)
    MiscTechWantToWorkWith = models.CharField(max_length=100)
    ToolsTechHaveWorkedWith = models.CharField(max_length=100)
    ToolsTechWantToWorkWith = models.CharField(max_length=100)
    NEWCollabToolsHaveWorkedWith = models.CharField(max_length=100)
    NEWCollabToolsWantToWorkWith = models.CharField(max_length=100)
    OpSys = models.CharField(max_length=100)
    NEWStuck = models.CharField(max_length=100)
    NEWSOSites = models.CharField(max_length=100)
    SOVisitFreq = models.CharField(max_length=100)
    SOAccount = models.CharField(max_length=100)
    SOPartFreq = models.CharField(max_length=100)
    SOComm = models.CharField(max_length=100)
    NEWOtherComms = models.CharField(max_length=100)
    Age = models.CharField(max_length=100)
    Gender = models.CharField(max_length=100)
    Trans = models.CharField(max_length=100)
    Sexuality = models.CharField(max_length=100)
    Ethnicity = models.CharField(max_length=100)
    Accessibility = models.CharField(max_length=100)
    MentalHealth = models.CharField(max_length=100)
    SurveyLength = models.CharField(max_length=100)
    SurveyEase = models.CharField(max_length=100)
    ConvertedCompYearly = models.CharField(max_length=100)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE, default=None, null=True)

    # The following logic are simple hacks due to the lack of boolean properties in the developer profile
    @admin.display(
        boolean=True,
        description='Considered Professional?',
    )
    def is_pro(self):
        return 'pro' in str.lower(self.MainBranch) and 'not a pro' not in str.lower(self.MainBranch)

    @admin.display(
        boolean=True,
        description='Frontend?',
    )
    def is_front(self):
        dev_langs = str.lower(self.WebframeHaveWorkedWith)
        for lang in ['angular', 'vue', 'react']:
            if lang in dev_langs:
                return True
        return False

    @admin.display(
        boolean=True,
        description='Backend?',
    )
    def is_back(self):
        dev_langs = str.lower(self.LanguageHaveWorkedWith)
        for lang in ['node', 'python', 'php', 'ruby']:
            if lang in dev_langs:
                return True
        return False

    @admin.display(
        boolean=True,
        description='Full stack?',
    )
    def is_full(self):
        return self.is_front() and self.is_back()

    @admin.display(
        boolean=True,
        description='Has an academic degree?',
    )
    def is_academic(self):
        # TODO: Ask for clarification: In the context of this question, is an academic developer considered to be
        # a person with an academic degree, or simply a developer just out of college, without prior experience?
        for degree in ['degree', 'ba', 'b.a', 'b.s', 'bs', 'b.e', 'be', 'bachelor', 'master', 'phd']:
            if degree in str.lower(self.EdLevel):
                return True
        return False
