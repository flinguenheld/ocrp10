from django.db import models

from authentication.models import User


class Project(models.Model):

    class TypeProject(models.TextChoices):
        BACK_END = 'Back-end'
        FRONT_END = 'Front-end'
        IOS = 'iOS'
        ANDROID = 'Android'

    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=2048, blank=True)
    type = models.CharField(choices=TypeProject.choices, max_length=50)
    time_created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"Project [{self.id} : {self.title} - {self.type}]"


class Contributor(models.Model):

    class Permission(models.TextChoices):
        CREATOR = 'Créateur'
        CONTRIBUTOR = 'Contributeur'

    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    permission = models.CharField(choices=Permission.choices,
                                  max_length=50,
                                  default=Permission.CONTRIBUTOR,
                                  editable=False)

    class Meta:
        # ContributorAddSerializer also checks this contraint
        constraints = [
            models.UniqueConstraint(fields=['project', 'user'],
                                    name='unique_contributor')
        ]

    def __str__(self):
        return f"Contrib [{self.id} : {self.user.email} - {self.permission}]"


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
    project = models.ForeignKey(to=Project,
                                on_delete=models.CASCADE,
                                related_name='issue_project')
    author = models.ForeignKey(to=User,
                                on_delete=models.CASCADE,
                                related_name='issue_author',
                                editable=False)
    assigned = models.ForeignKey(to=User,
                                 on_delete=models.CASCADE,
                                 related_name='issue_assigned')
                                 # editable=False)  # Impossible ?

    priority = models.CharField(choices=Priority.choices,
                                max_length=50,
                                default=Priority.MEDIUM)
    status = models.CharField(choices=Status.choices,
                              max_length=50,
                              default=Status.TO_DO)
    tag = models.CharField(choices=Tag.choices,
                           max_length=50,
                           default=Tag.TASK)
    time_created = models.DateTimeField(auto_now_add=True,
                                        editable=False)

    def __str__(self):
        return f"Issue [{self.title} - {self.project}]"

class Comment(models.Model):

    description = models.CharField(max_length=2048)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE,
                               editable=False)
    issue = models.ForeignKey(to=Issue,
                              on_delete=models.CASCADE)
                              # editable=False)
    time_created = models.DateTimeField(auto_now_add=True,
                                        editable=False)

    def __str__(self):
        return f"Comment [{self.description} - {self.author} - {self.issue}]"
