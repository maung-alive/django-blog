# Generated by Django 4.2.2 on 2023-12-06 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_remove_action_action_remove_action_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='type',
            field=models.CharField(default='i', max_length=1),
            preserve_default=False,
        ),
    ]