# Generated by Django 4.2.5 on 2023-10-15 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_four', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10),
        ),
    ]
