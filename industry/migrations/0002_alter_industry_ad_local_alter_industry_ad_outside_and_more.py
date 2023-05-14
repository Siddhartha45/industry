# Generated by Django 4.1 on 2023-04-23 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industry',
            name='ad_local',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='industry',
            name='ad_outside',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='industry',
            name='bank_current',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='industry',
            name='bank_fixed',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='industry',
            name='industry_photo',
            field=models.ImageField(blank=True, upload_to='image'),
        ),
        migrations.AlterField(
            model_name='industry',
            name='self_current',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='industry',
            name='self_fixed',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='industry',
            name='technical_local',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='industry',
            name='technical_outside',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
