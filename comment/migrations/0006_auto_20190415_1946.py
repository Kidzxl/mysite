# Generated by Django 2.0 on 2019-04-15 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0005_auto_20190330_1548'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['comment_time']},
        ),
    ]
