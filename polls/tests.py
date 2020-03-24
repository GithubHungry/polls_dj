import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


# Create your tests here.

class QuestionModelTests(TestCase):

	def test_recently_future(self):
		"""Future posting (recently)."""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""Older than 1 day"""
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		"""One day recent question"""
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
	"""Create 1 question."""
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
	def test_no_question(self):
		"""If there is no question."""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'No polls are available.')
		self.assertQuerysetEqual(response.context['polls'], [])

	def test_past_question(self):
		"""Pub_date in the past."""
		create_question(question_text='Past question', days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['polls'], ['<Question: Past question>'])

	def test_future_question(self):
		"""Pub_date in the future."""
		create_question(question_text='Future question', days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['polls'], [])

	def test_future_past_questions(self):
		"""Pub_date in the future and one in the past."""
		create_question(question_text='Past question', days=-30)
		create_question(question_text='Future question', days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['polls'], ['<Question: Past question>'])

	def test_past_past_questions(self):
		"""Pub_date in the past and one more in the past."""
		create_question(question_text='Past question 1', days=-30)
		create_question(question_text='Past question 2', days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['polls'],
		                         ['<Question: Past question 1>', '<Question: Past question 2>'])


class QuestionDetailViewTests(TestCase):
	def test_future_question(self):
		"""Future questions return 404."""
		future_question = create_question(question_text='Future question', days=5)
		url = reverse('polls:detail', args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_past_question(self):
		"""Check normal past question."""
		past_question = create_question(question_text='Past_question', days=-5)
		response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, past_question.question_text)
