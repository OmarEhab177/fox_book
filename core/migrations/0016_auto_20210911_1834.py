# Generated by Django 3.1 on 2021-09-11 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20210910_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactreplies',
            name='contact_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.newcontact'),
        ),
    ]
