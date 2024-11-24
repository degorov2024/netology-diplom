# Generated by Django 5.0.2 on 2024-11-22 14:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('text', models.TextField(blank=True)),
                ('image', models.ImageField(null=True, upload_to='posts')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_post', to='posts.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented_post', to='posts.post')),
            ],
        ),
    ]
