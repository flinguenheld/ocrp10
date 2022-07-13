# Generated by Django 4.0.5 on 2022-07-13 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_management', '0010_alter_issue_assigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assigned',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_assigned', to=settings.AUTH_USER_MODEL),
        ),
    ]
