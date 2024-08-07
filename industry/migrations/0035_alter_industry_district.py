# Generated by Django 4.1 on 2023-08-01 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industry', '0034_alter_industry_investment_alter_industry_reg_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industry',
            name='district',
            field=models.CharField(blank=True, choices=[('KAILALI', 'कैलाली'), ('KANCHANPUR', 'कञ्चनपुर'), ('DADELDHURA', 'डडेल्धुरा'), ('DOTI', 'डोटी'), ('ACHHAM', 'अछाम'), ('BAJURA', 'बाजुरा'), ('BAJHANG', 'बझाङ'), ('BAITADI', 'बैतडी'), ('DARCHULA', 'दार्चुला')], max_length=20, null=True),
        ),
    ]
