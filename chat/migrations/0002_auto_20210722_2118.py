# Generated by Django 3.2 on 2021-07-22 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_name',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(default='defaul_user', max_length=150),
            preserve_default=False,
        ),
    ]
