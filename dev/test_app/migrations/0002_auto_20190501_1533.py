# Generated by Django 2.2 on 2019-05-01 12:33

from django.db import migrations, models


class Migration(migrations.Migration):
	dependencies = [
		('test_app', '0001_initial'),
	]

	operations = [
		migrations.RemoveField(
			model_name='author',
			name='birth_date',
		),
		migrations.RemoveField(
			model_name='author',
			name='title',
		),
		migrations.AlterField(
			model_name='author',
			name='name',
			field=models.CharField(max_length=200),
		),
	]
