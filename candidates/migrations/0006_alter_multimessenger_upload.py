# Generated by Django 3.2.9 on 2022-02-28 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0005_auto_20220228_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multimessenger',
            name='upload',
            field=models.FileField(blank=True, upload_to='uploads/', verbose_name='Uploaded File'),
        ),
    ]