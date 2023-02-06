# Generated by Django 3.1.12 on 2021-10-10 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('displaycode', '0011_auto_20200608_0512'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitListUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('username', models.TextField()),
                ('aboutme', models.TextField()),
                ('painpoints', models.TextField()),
                ('joinedDate', models.DateTimeField(blank=True, null=True)),
                ('referralUrl', models.TextField()),
            ],
        ),
    ]