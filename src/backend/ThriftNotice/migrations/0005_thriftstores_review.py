# Generated by Django 5.1.6 on 2025-02-27 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ThriftNotice', '0004_remove_thriftstores_isestablishedstore_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='thriftstores',
            name='review',
            field=models.TextField(blank=True, db_column='Review', null=True),
        ),
    ]
