# Generated by Django 2.0.4 on 2018-05-05 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemes', '0013_auto_20180502_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='KurnikRanking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.CharField(max_length=20)),
                ('games', models.CharField(max_length=6)),
                ('ranking', models.CharField(max_length=4)),
            ],
        ),
    ]
