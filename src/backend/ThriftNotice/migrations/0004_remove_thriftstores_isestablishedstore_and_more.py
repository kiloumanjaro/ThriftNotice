# Generated by Django 5.1.6 on 2025-02-27 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ThriftNotice', '0003_alter_thriftstores_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thriftstores',
            name='isestablishedstore',
        ),
        migrations.RemoveField(
            model_name='thriftstores',
            name='ispopupevent',
        ),
        migrations.AlterField(
            model_name='thriftstores',
            name='popupstarttime',
            field=models.TimeField(blank=True, db_column='PopUpStartTime', null=True),
        ),
    ]
