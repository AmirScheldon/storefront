# Generated by Django 5.0.1 on 2024-01-30 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('can_cancel', 'Can cancel order')]},
        ),
    ]
