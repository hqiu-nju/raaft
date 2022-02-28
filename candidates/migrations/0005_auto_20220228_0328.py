# Generated by Django 3.2.9 on 2022-02-28 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0004_auto_20220228_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multimessenger',
            name='choice_text',
            field=models.CharField(max_length=200, verbose_name='Info'),
        ),
        migrations.AlterField(
            model_name='multimessenger',
            name='upload',
            field=models.ImageField(blank=True, upload_to='uploads/', verbose_name='Uploaded Image'),
        ),
    ]