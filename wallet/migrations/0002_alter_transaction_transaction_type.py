# Generated by Django 5.1.3 on 2024-11-11 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('deposit', 'deposit'), ('withdraw', 'withdraw'), ('purchase', 'purchase')], max_length=20),
        ),
    ]
