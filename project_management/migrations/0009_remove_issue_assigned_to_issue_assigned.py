# Generated by Django 4.0.5 on 2022-07-13 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_management', '0008_alter_comment_author_alter_comment_issue_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='assigned_to',
        ),
        migrations.AddField(
            model_name='issue',
            name='assigned',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issue_assigned', to=settings.AUTH_USER_MODEL),
        ),
    ]
