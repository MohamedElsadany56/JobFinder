# Generated by Django 4.2.17 on 2024-12-16 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_task_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('Task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apply_task', to='task.task')),
            ],
        ),
    ]