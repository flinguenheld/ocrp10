# Generated by Django 4.0.5 on 2022-07-14 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0012_alter_comment_issue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='creator',
            new_name='author',
        ),
    ]
