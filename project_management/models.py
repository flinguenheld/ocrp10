from django.db import models

from authentication.models import User


class Project(models.Model):

    class TypeProject(models.TextChoices):
        BACK_END = 'Back-end'
        FRONT_END = 'Front-end'
        IOS = 'iOS'
        ANDROID = 'Android'

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    type = models.CharField(choices=TypeProject.choices, max_length=50)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.type}"


class Contributor(models.Model):

    class Role(models.TextChoices):
        CREATOR = 'Créateur'
        CONTRIBUTOR = 'Contributeur'

    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    permission = models.CharField(choices=Role.choices, max_length=50, default=Role.CONTRIBUTOR)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['project', 'user'], name='unique_contributor')
        ]

    def __str__(self):
        return f"{self.user.email} - {self.permission} - {self.project}"


class Issue(models.Model):

    class Priority(models.TextChoices):
        LOW = 'Faible'
        MEDIUM = 'Moyenne'
        HIGH = 'Élevée'

    class Status(models.TextChoices):
        TO_DO = 'À faire'
        IN_PROGRESS = 'En cours'
        DONE = 'Terminé'

    class Tag(models.TextChoices):
        BUG = 'Bug'
        TASK = 'Tâche'
        UPGRADE = 'Amélioration'

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    creator = models.ForeignKey(to=User,
                                on_delete=models.CASCADE,
                                related_name='user_creator')
    assigned_to = models.ForeignKey(to=User,
                                    on_delete=models.CASCADE,
                                    related_name='assigned_to_user',
                                    null=True) 
    priority = models.CharField(choices=Priority.choices, max_length=50)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices, max_length=50)
    tag = models.CharField(choices=Tag.choices, max_length=50)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.project}"

class Comment(models.Model):

    description = models.CharField(max_length=2048)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment : {self.issue} - {self.issue}"
