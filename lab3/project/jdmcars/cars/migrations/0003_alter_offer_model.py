# Generated by Django 3.2.3 on 2021-05-31 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_alter_offer_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.model'),
        ),
    ]