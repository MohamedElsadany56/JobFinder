# Generated by Django 4.2.17 on 2024-12-20 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_apply_experience_apply_required_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apply',
            old_name='required_price',
            new_name='desired_price',
        ),
    ]