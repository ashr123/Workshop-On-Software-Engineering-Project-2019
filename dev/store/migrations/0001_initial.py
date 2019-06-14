# Generated by Django 2.2.2 on 2019-06-14 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('items', models.ManyToManyField(to='store.Item')),
                ('managers', models.ManyToManyField(related_name='store_managers', to=settings.AUTH_USER_MODEL)),
                ('owners', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('ADD_ITEM', 'add item'), ('REMOVE_ITEM', 'delete item'), ('EDIT_ITEM', 'update item'), ('ADD_MANAGER', 'add manager'), ('REMOVE_STORE', 'delete store'), ('ADD_DISCOUNT', 'add discount')),
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('MXQ', 'max_quantity'), ('MNQ', 'min_quantity')], max_length=3, null=True)),
                ('amount', models.IntegerField(default=0, null=True)),
                ('end_date', models.DateField(help_text='format: mm/dd/yyyy')),
                ('percentage', models.PositiveSmallIntegerField()),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Item')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Store')),
            ],
        ),
        migrations.CreateModel(
            name='ComplexStoreRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left', models.CharField(max_length=4)),
                ('right', models.CharField(max_length=4)),
                ('operator', models.CharField(choices=[('OR', 'or'), ('AND', 'and'), ('XOR', 'xor')], max_length=3)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Store')),
            ],
        ),
        migrations.CreateModel(
            name='ComplexItemRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left', models.CharField(max_length=4)),
                ('right', models.CharField(max_length=4)),
                ('operator', models.CharField(choices=[('OR', 'or'), ('AND', 'and'), ('XOR', 'xor')], max_length=3)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Item')),
            ],
        ),
        migrations.CreateModel(
            name='BaseRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('MXQ', 'max_quantity'), ('MNQ', 'min_quantity'), ('RGO', 'registered_only'), ('FBC', 'forbidden_countries')], max_length=3)),
                ('parameter', models.CharField(max_length=120)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Store')),
            ],
        ),
        migrations.CreateModel(
            name='BaseItemRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('MXQ', 'max_quantity'), ('MNQ', 'min_quantity')], max_length=3)),
                ('parameter', models.CharField(max_length=120)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Item')),
            ],
        ),
    ]
