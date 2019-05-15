# Generated by Django 2.2.1 on 2019-05-14 17:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('name', models.CharField(default=None, max_length=30)),
                ('description', models.CharField(default=None, max_length=64)),
                ('category', models.CharField(choices=[('1', 'ALL'), ('2', 'HOME'), ('3', 'WORK')], default=1, max_length=30)),
                ('quantity', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=64)),
                ('discount', models.PositiveIntegerField(default=0)),
                ('items', models.ManyToManyField(to='store.Item')),
                ('owners', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('ADD_ITEM', 'add item'), ('REMOVE_ITEM', 'delete item'), ('EDIT_ITEM', 'update item'), ('ADD_MANAGER', 'add manager'), ('REMOVE_STORE', 'delete store')),
            },
        ),
    ]
