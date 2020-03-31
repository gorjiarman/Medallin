# Generated by Django 3.0.4 on 2020-03-24 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('predicting', '0008_auto_20200324_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.CharField(max_length=16, primary_key=True, serialize=False, verbose_name='شناسه')),
                ('type', models.CharField(choices=[('disease', 'بیماری'), ('symptom', 'علامت')], max_length=16, verbose_name='نوع شناسه')),
            ],
            options={
                'verbose_name': 'شناسه',
                'verbose_name_plural': 'شناسه\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locale', models.CharField(choices=[('en-us', 'English (United States)'), ('fa-ir', 'فارسی (ایران)')], max_length=5, verbose_name='زبان')),
                ('string', models.CharField(max_length=128, verbose_name='رشته')),
                ('concept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='predicting.Concept', verbose_name='شناسه')),
            ],
            options={
                'verbose_name': 'ترجمه',
                'verbose_name_plural': 'ترجمه\u200cها',
            },
        ),
        migrations.CreateModel(
            name='DiseaseFrequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.PositiveIntegerField(verbose_name='فراوانی')),
                ('concept', models.ForeignKey(limit_choices_to=models.Q(type='disease'), on_delete=django.db.models.deletion.CASCADE, to='predicting.Concept', verbose_name='شناسه')),
            ],
            options={
                'verbose_name': 'فراوانی بیماری',
                'verbose_name_plural': 'فراوانی\u200cهای بیماری\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.TextField(verbose_name='شرط')),
                ('factor', models.FloatField(verbose_name='ضریب')),
                ('concept', models.ForeignKey(limit_choices_to=models.Q(type='disease'), on_delete=django.db.models.deletion.CASCADE, to='predicting.Concept', verbose_name='شناسه')),
            ],
            options={
                'verbose_name': 'شرط',
                'verbose_name_plural': 'شرایط',
            },
        ),
    ]