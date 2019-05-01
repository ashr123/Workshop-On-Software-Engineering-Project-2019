# Generated by Django 2.2 on 2019-05-01 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
	initial = True

	dependencies = [
	]

	operations = [
		migrations.CreateModel(
			name='Author',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('name', models.CharField(max_length=100)),
				('title', models.CharField(choices=[('MR', 'Mr.'), ('MRS', 'Mrs.'), ('MS', 'Ms.')], max_length=3)),
				('birth_date', models.DateField(blank=True, null=True)),
			],
		),
		migrations.CreateModel(
			name='Reporter',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('full_name', models.CharField(max_length=70)),
			],
		),
		migrations.CreateModel(
			name='Book',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('name', models.CharField(max_length=100)),
				('authors', models.ManyToManyField(to='test_app.Author')),
			],
		),
		migrations.CreateModel(
			name='Article',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('pub_date', models.DateField()),
				('headline', models.CharField(max_length=200)),
				('content', models.TextField()),
				('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_app.Reporter')),
			],
		),
	]