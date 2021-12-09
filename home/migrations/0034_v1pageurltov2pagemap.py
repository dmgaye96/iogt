# Generated by Django 3.1.13 on 2021-12-02 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0059_apply_collection_ordering'),
        ('home', '0033_merge_20211201_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='V1PageURLToV2PageMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('v1_page_url', models.CharField(max_length=255)),
                ('v2_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.page')),
            ],
        ),
    ]