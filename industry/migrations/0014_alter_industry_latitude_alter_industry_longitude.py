# Generated by Django 4.1 on 2023-04-28 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industry', '0013_alter_industry_caste_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industry',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='industry',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=20, null=True),
        ),
    ]
