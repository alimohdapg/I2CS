# Generated by Django 4.1.3 on 2022-11-25 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0005_alter_evaluations_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evaluations',
            old_name='user_id',
            new_name='user',
        ),
    ]