from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('examprep_app', '01_init'),    #_app   .User
    ]
    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('favoritor', models.ManyToManyField(related_name='fav_items', to='examprep_app.User')),    #_app   .User
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_uploaded', to='examprep_app.User')),    #_app   .User
            ],
        ),
    ]
