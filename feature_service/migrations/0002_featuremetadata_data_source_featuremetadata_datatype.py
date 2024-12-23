# Generated by Django 5.1.2 on 2024-10-13 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='featuremetadata',
            name='data_source',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='featuremetadata',
            name='datatype',
            field=models.CharField(choices=[('STRING', 'String'), ('INT', 'Integer'), ('FLOAT', 'Float'), ('ARRAY_STRING', 'ArrayString'), ('ARRAY_INT', 'ArrayInt'), ('ARRAY_FLOAT', 'ArrayFloat')], default='STRING', max_length=250),
        ),
    ]
