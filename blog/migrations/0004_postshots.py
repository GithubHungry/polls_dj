# Generated by Django 3.0.4 on 2020-03-25 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_poster'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostShots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='book_shots/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post', verbose_name='Post')),
            ],
            options={
                'verbose_name': 'Post image',
                'verbose_name_plural': 'Post images',
            },
        ),
    ]