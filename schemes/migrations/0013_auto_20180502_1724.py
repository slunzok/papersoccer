# Generated by Django 2.0.4 on 2018-05-02 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemes', '0012_auto_20180502_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='replay',
            name='name',
            field=models.CharField(default='do-zmiany', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scheme',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]