# Generated by Django 4.1 on 2023-04-24 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='aa', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
