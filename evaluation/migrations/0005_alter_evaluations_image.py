# Generated by Django 4.1.3 on 2022-11-24 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0004_evaluations_user_id_alter_evaluations_contact_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluations',
            name='image',
            field=models.ImageField(upload_to='evaluation/images/'),
        ),
    ]
