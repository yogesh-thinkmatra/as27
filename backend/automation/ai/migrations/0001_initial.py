# Generated by Django 4.1.1 on 2023-10-27 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Electricians',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=50)),
                ('grievance', models.BooleanField(blank=True, default=False)),
            ],
            options={
                'db_table': 'electricians',
            },
        ),
        migrations.CreateModel(
            name='Sites',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=50)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('installation_date', models.DateField(blank=True)),
                ('grievance', models.BooleanField(blank=True, default=False)),
            ],
            options={
                'db_table': 'sites',
            },
        ),
        migrations.CreateModel(
            name='SitesAllocation',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('electrician', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ai.electricians')),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ai.sites')),
            ],
            options={
                'db_table': 'sites_allocation',
            },
        ),
    ]
