from django.db import models
from django.conf import settings

class Label(models.Model):
    theme = models.CharField(max_length=20)
    def questions(self):
        return Question.objects.filter(label=self)
    def __str__(self):
        return self.theme

class Userr(models.Model):
    name = models.CharField(max_length=80)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def results(self):
        return Result.objects.filter(userr=self)
    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.CharField(max_length=200, unique=True)
    pub_date = models.DateTimeField('Pub Date')
    label = models.ForeignKey(Label, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(Userr, on_delete=models.DO_NOTHING)
    score = models.IntegerField()
    def options(self):
        return Option.objects.filter(question=self)
    def __str__(self):
        return self.text

class Quiz(models.Model):
    title = models.CharField(max_length=200, unique=True)
    pub_date = models.DateTimeField('Pub Date')
    author = models.ForeignKey(Userr, on_delete=models.DO_NOTHING)
    question = models.ManyToManyField(Question, blank=True, null=True, related_name='quiz')
    def questions(self):
        return Question.objects.filter(quiz=self)
    def __str__(self):
        return self.title

class Option(models.Model):
    text = models.CharField(max_length=100)
    correct = models.BooleanField(default = False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    def __str__(self):
        return self.text

class Result(models.Model):
    grade = models.FloatField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    userr = models.ForeignKey(Userr, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Pub Date')
    def __str__(self):
        return self.userr
