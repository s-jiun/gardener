# Generated by Django 3.2.6 on 2021-08-15 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Postviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='조회날짜')),
                ('client_ip', models.GenericIPAddressField(null=True, verbose_name='사용자 Ip주소')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.post', verbose_name='조회한 게시물')),
            ],
        ),
    ]
