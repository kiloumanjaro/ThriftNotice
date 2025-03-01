# Generated by Django 5.1.6 on 2025-02-28 19:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ThriftNotice', '0007_merge_20250301_0303'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='usernmae',
            field=models.TextField(blank=True, db_column='username', null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='budget',
            field=models.TextField(blank=True, db_column='budget', null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='clothing',
            field=models.TextField(blank=True, db_column='clothing', null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='interest',
            field=models.TextField(blank=True, db_column='interest', null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='organization',
            field=models.TextField(blank=True, db_column='organization', null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='shoppingenvironment',
            field=models.TextField(blank=True, db_column='shoppingenvironment', null=True),
        ),
        migrations.CreateModel(
            name='FavoriteShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopid', models.ForeignKey(db_column='shopid', on_delete=django.db.models.deletion.CASCADE, to='ThriftNotice.thriftstores')),
                ('userid', models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.CASCADE, to='ThriftNotice.users')),
            ],
            options={
                'db_table': 'favorite_shops',
                'db_table_comment': 'A table storing favorite shops for each user.',
                'unique_together': {('userid', 'shopid')},
            },
        ),
    ]
