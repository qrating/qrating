# Generated by Django 2.2.3 on 2019-08-22 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190822_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.CharField(choices=[('economy', '경제학'), ('programming', '프로그래밍'), ('math', '수학'), ('management', '경영학'), ('cpa', 'CPA/고시'), ('etc', '기타')], default='economy', max_length=15),
        ),
    ]