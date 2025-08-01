# Generated by Django 4.2.17 on 2025-07-05 09:40

from django.db import migrations, models
import recipient.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllocatedDonorToRecipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verification_status', models.BooleanField(default=False)),
                ('verification_token', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('token_expiry', models.DateTimeField(default=recipient.models.one_day_from_now)),
                ('allocation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.FloatField()),
                ('gender', models.IntegerField(choices=[(0, 'Female'), (1, 'Male')])),
                ('blood_type', models.CharField(max_length=3)),
                ('rh_factor', models.IntegerField(choices=[(0, 'Negative'), (1, 'Positive')])),
                ('height_cm', models.FloatField()),
                ('weight_kg', models.FloatField()),
                ('bmi', models.FloatField()),
                ('wait_list_days', models.IntegerField()),
                ('medical_urgency_score', models.FloatField()),
                ('hemoglobin', models.FloatField()),
                ('wbc_count', models.FloatField()),
                ('platelet_count', models.FloatField()),
                ('creatinine', models.FloatField()),
                ('alt', models.FloatField()),
                ('ast', models.FloatField()),
                ('diabetes', models.IntegerField(choices=[(0, 'No'), (1, 'Yes')])),
                ('hypertension', models.IntegerField(choices=[(0, 'No'), (1, 'Yes')])),
                ('previous_transplant', models.IntegerField(choices=[(0, 'No'), (1, 'Yes')])),
                ('dialysis_status', models.IntegerField(choices=[(0, 'No'), (1, 'Yes')])),
                ('required_organ', models.CharField(max_length=50)),
                ('antibody_screen', models.FloatField()),
                ('pra_score', models.FloatField()),
                ('transplant_eligibility', models.CharField(default='not eligible', max_length=50)),
            ],
        ),
    ]
