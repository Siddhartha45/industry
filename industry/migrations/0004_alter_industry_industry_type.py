# Generated by Django 4.1 on 2023-04-23 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industry', '0003_alter_industry_ad_local_alter_industry_ad_outside_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industry',
            name='industry_type',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=10),
        ),
    ]
