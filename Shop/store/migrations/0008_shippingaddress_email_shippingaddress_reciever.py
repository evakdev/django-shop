# Generated by Django 4.0.1 on 2022-01-18 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_shippingaddress_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='email',
            field=models.EmailField(default='as', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='reciever',
            field=models.CharField(default='as', max_length=150),
            preserve_default=False,
        ),
    ]
