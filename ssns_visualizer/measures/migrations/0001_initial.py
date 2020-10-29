# Generated by Django 3.1.2 on 2020-10-26 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('light', models.IntegerField()),
                ('range', models.IntegerField()),
            ],
        ),
    ]