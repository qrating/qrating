# Generated by Django 2.2.3 on 2019-07-28 10:19

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_answer_image_question_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', imagekit.models.fields.ProcessedImageField(upload_to='images/')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', imagekit.models.fields.ProcessedImageField(upload_to='images/')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Question')),
            ],
        ),
        migrations.RemoveField(
            model_name='question_image',
            name='post',
        ),
        migrations.DeleteModel(
            name='Answer_Image',
        ),
        migrations.DeleteModel(
            name='Question_Image',
        ),
    ]
