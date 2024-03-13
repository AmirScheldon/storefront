# Generated by Django 5.0.3 on 2024-03-05 08:49

import django.core.validators
import store.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='store/media', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg']), store.validator.validate_image_size]),
        ),
    ]
