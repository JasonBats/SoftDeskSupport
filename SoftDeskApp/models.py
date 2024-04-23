from django.db import models
from SoftDeskSupport.settings import AUTH_USER_MODEL


class Project(models.Model):
    BACK_END = 'Back-end'
    FRONT_END = 'Front-end'
    IOS = 'iOS'
    ANDROID = 'Android'

    TYPE_CHOICES = (
        (BACK_END, 'Back-end'),
        (FRONT_END, 'Front-end'),
        (IOS, 'iOS'),
        (ANDROID, 'Android')
    )

    name = models.CharField(max_length=120, blank=False, null=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=25, choices=TYPE_CHOICES, verbose_name='Type', blank=False, null=False)

    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False, related_name='Author_of')
    contributors = models.ManyToManyField(AUTH_USER_MODEL, through='Contributor', related_name='Contributor_of')

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Issue(models.Model):
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'

    PRIORITY_CHOICES = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )

    BUG = 'BUG'
    FEATURE = 'FEATURE'
    TASK = 'TASK'

    NATURE_CHOICES = (
        (BUG, 'Bug'),
        (FEATURE, 'Feature'),
        (TASK, 'Task')
    )

    TO_DO = 'To do'
    IN_PROGRESS = 'In progress'
    FINISHED = 'Finished'

    STATUS_CHOICES = (
        (TO_DO, 'To do'),
        (IN_PROGRESS, 'In progress'),
        (FINISHED, 'Finished')

    )

    name = models.CharField(max_length=120, blank=False, null=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_issues', null=False, blank=False)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='Issues',
        null=False,
        blank=False
    )

    assigned_to = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_issues'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        verbose_name='Priority',
        blank=False, null=False,
        default=MEDIUM
    )

    nature = models.CharField(
        max_length=20,
        choices=NATURE_CHOICES,
        verbose_name='Nature',
        blank=False,
        null=False,
        default=TASK
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name='Status',
        blank=False,
        null=False,
        default=TO_DO
    )


class Comment(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    description = models.TextField(max_length=500, blank=False, null=False)


class Contributor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
