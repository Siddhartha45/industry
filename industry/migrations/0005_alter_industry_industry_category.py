# Generated by Django 4.1 on 2023-04-23 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industry', '0004_alter_industry_industry_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industry',
            name='industry_category',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=10),
        ),
    ]
