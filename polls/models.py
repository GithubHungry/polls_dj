import datetime

from django.utils import timezone

from django.db import models


# Create your models here.
class Question(models.Model):
	"""Model for question."""
	question_text = models.CharField(max_length=225)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
	"""Model for choice."""
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=225)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text
