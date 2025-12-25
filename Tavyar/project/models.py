from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=300)
    github_url = models.URLField(blank=True, null=True)
    live_demo = models.URLField(blank=True, null=True)
    image = models.URLField(blank=True, null=True, verbose_name='لینک تصویر پروژه', max_length=500, help_text='لطفا لینک تصویر پروژه از ابرآروان را قرار دهید')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title