# Generated by Django 3.1.14 on 2021-12-17 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0003_message_is_post_processed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatbotchannel',
            name='display_name',
            field=models.CharField(help_text='Name for the bot that the user will see when interacting with it', max_length=80),
        ),
        migrations.AlterField(
            model_name='chatbotchannel',
            name='request_url',
            field=models.URLField(help_text='To set up a chatbot channel on your RapidPro server and get a request URL, follow the steps outline in the Section "Setting up a Chatbot channel" here: https://github.com/unicef/iogt/blob/develop/messaging/README.md'),
        ),
    ]