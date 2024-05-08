# Generated by Django 4.2 on 2024-04-11 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_header', models.CharField(max_length=100)),
                ('activity_content', models.TextField()),
                ('activity_image', models.ImageField(upload_to='activities/')),
                ('activity_is_active', models.BooleanField(default=False)),
                ('activity_date', models.DateTimeField()),
                ('activity_club', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school_app.club')),
            ],
        ),
    ]
