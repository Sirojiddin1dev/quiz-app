from django.db import models
from django.urls import reverse
from django.conf import settings
from customusers.models import CustomUser 

TOGRI = (
    ('a', 'a'),
    ('b', 'b'),
    ('c', 'c'),
    ('d', 'd')
)


class Category(models.Model):
    TASK_TYPE = (
    ('1-2-Modul', '1-2-Modul'),
    ('3-Modul', '3-Modul'),
    )
    title = models.CharField(max_length=150, choices=TASK_TYPE)
    count_task = models.IntegerField()
    is_active = models.BooleanField(default=False)
    timer = models.IntegerField(default=1, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title == "1-2-Modul":
            self.timer = 43
        else:
            self.timer = 86
        super(Category, self).save(*args, **kwargs)


class Task(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    a = models.CharField(max_length=150)
    b = models.CharField(max_length=150)
    c = models.CharField(max_length=150)
    d = models.CharField(max_length=150)
    togri_javob = models.CharField(max_length=30, choices=TOGRI, default='a')
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('admindetail', kwargs={'id': self.category.id})


class Taskusers(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=1)
    category = models.ForeignKey(Category, editable=False, on_delete=models.CASCADE)
    natija1 = models.IntegerField(null=True, blank=True)
    checking = models.CharField(max_length=10, null=True, blank=True)
    natija2 = models.IntegerField(null=True, blank=True)
    checking2 = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    all = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ('all', "-natija1", "-natija2")

    def __str__(self):
        count_task = self.category.count_task
        all = self.all
        if count_task:
            if all == 'ALL':
                procent1 = round((self.natija1 or 0) / 26 * 100, 2)
                procent2 = round((self.natija2 or 0) / 65 * 100, 2)
                count_task = 91
            else:
                procent1 = round((self.natija1 or 0) / count_task * 100, 2)
                procent2 = round((self.natija2 or 0) / count_task * 100, 2)
        else:
            procent1 = 0
            procent2 = 0
        return f"Task count: {count_task}. Correct answer 1: {self.natija1}. Percent 1: {procent1}%. Correct answer 2: {self.natija2}. Percent 2: {procent2}%"
