# Generated by Django 4.1 on 2023-04-27 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industry', '0010_alter_product_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='industry',
            old_name='capacity_of_industry_operation',
            new_name='current_running_capacity',
        ),
        migrations.RenameField(
            model_name='industry',
            old_name='established_date',
            new_name='reg_date',
        ),
        migrations.RenameField(
            model_name='industry',
            old_name='phone_number',
            new_name='telephone_number',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='ad_local',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='ad_outside',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='bank_current',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='bank_fixed',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='expectations_with_gov',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='industry_capital',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='industry_category',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='industry_type',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='key_challanges',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='local_government',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='name_of_machine_tool',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='nature_of_investment',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='product_name',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='renew_expire_date',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='self_current',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='self_fixed',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='tax_status',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='technical_local',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='technical_outside',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='tole',
        ),
        migrations.RemoveField(
            model_name='industry',
            name='type_of_product_based_on_industry',
        ),
        migrations.AddField(
            model_name='industry',
            name='address',
            field=models.CharField(default='address', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='caste',
            field=models.CharField(choices=[('DALIT', 'DALIT'), ('JANAJATI', 'JANAJATI'), ('OTHERS', 'OTHERS')], default='DALIT', max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='current_capital',
            field=models.CharField(default='3000', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='female',
            field=models.CharField(default='30', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='fixed_capital',
            field=models.CharField(default='30', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='foreign',
            field=models.CharField(default='30', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='indigenous',
            field=models.CharField(default='30', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='industry_acc_product',
            field=models.CharField(choices=[('E', 'ENERGY'), ('MF', 'MANUFACTURING'), ('AF', 'AGRICULTURE OR FORESTRY BASED'), ('MI', 'MINERAL'), ('I', 'INFRASTRUCTURE'), ('T', 'TOURISM'), ('IC', 'INFORMATION AND COMMUNICATION'), ('S', 'SERVICE'), ('O', 'Others')], default='E', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='industry_reg_no',
            field=models.CharField(default='2000', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='investment',
            field=models.CharField(choices=[('MINIATURE', 'MINIATURE'), ('DOMESTIC', 'DOMESTIC'), ('SMALL', 'SMALL'), ('MEDIUM', 'MEDIUM'), ('LARGE', 'LARGE')], default='SMALL', max_length=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='local_body',
            field=models.CharField(default='AB', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='machinery_tool',
            field=models.TextField(default='AAA', max_length=600),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='male',
            field=models.CharField(default='30', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='ownership',
            field=models.CharField(choices=[('PRIVATE', 'PRIVATE'), ('PARTNERSHIP', 'PARTNERSHIP')], default=1, max_length=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='product_description',
            field=models.TextField(default='aaa', max_length=600),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='product_service_name',
            field=models.CharField(default='dd', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='settlement',
            field=models.CharField(default='dd', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='sex',
            field=models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHERS', 'OTHERS')], default='MALE', max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='skillfull',
            field=models.CharField(default='30', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='total_capital',
            field=models.CharField(default='400', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='total_manpower',
            field=models.CharField(default='60', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='unskilled',
            field=models.CharField(default='40', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='industry',
            name='yearly_capacity',
            field=models.CharField(default='40', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='industry',
            name='contact_person',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='industry',
            name='current_status',
            field=models.CharField(choices=[('A', 'Active'), ('I', 'Inactive')], max_length=8),
        ),
        migrations.AlterField(
            model_name='industry',
            name='industry_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='industry',
            name='owner_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='industry',
            name='raw_material_source',
            field=models.CharField(choices=[('LOCAL', 'LOCAL'), ('IMPORTED', 'IMPORTED')], max_length=8),
        ),
        migrations.AlterField(
            model_name='industry',
            name='ward_no',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
