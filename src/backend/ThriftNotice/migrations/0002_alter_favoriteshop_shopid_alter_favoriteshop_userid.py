# Generated by Django 5.1.6 on 2025-03-04 13:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ThriftNotice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriteshop',
            name='shopid',
            field=models.ForeignKey(db_column='shopID', on_delete=django.db.models.deletion.CASCADE, to='ThriftNotice.thriftstores'),
        ),
        migrations.AlterField(
            model_name='favoriteshop',
            name='userid',
            field=models.ForeignKey(db_column='userID', on_delete=django.db.models.deletion.CASCADE, to='ThriftNotice.users'),
        ),
    ]
