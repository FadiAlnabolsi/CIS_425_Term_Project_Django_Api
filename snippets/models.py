from django.db import models
from django.db.models import Max

from django.contrib.auth.models import User

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


# Create your models here.


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

class Registrations(models.Model):
	firstName = models.CharField(verbose_name = 'First Name', max_length=50)
	lastName = models.CharField(verbose_name = 'Last Name', max_length=50)
	studentNumber = models.CharField(verbose_name = 'Student Number', max_length=8)
	emailaddress = models.TextField(verbose_name = 'Email')
	phoneNumber = models.CharField(verbose_name = 'Phone Number', max_length=10)
	dob_day = models.CharField(verbose_name = 'Date Of Birth - Day', max_length=2)
	dob_month = models.CharField(verbose_name = 'Date Of Birth - Month', max_length=2)
	dob_year = models.CharField(verbose_name = 'Date Of Birth - Year', max_length=4)
	registration_day = models.CharField(max_length=2)
	registration_month = models.CharField(max_length=2)
	registration_year = models.CharField(max_length=4)
	gender = models.CharField(verbose_name = 'Gender', max_length=1)
	collegeStatus = models.CharField(verbose_name = 'College Status', max_length=2)
	cumGpa = models.CharField(verbose_name = 'Cumulative GPA', max_length=4)
	currGpa = models.CharField(verbose_name = 'Semester GPA', max_length=4)
	numCredits = models.CharField(verbose_name = 'Number of Credits', max_length=3)
	winner = models.BooleanField(default=False)
	
	def __str__(self):
		return self.firstName + ' ' + self.lastName

	class Meta:
		verbose_name = 'Registration'
		verbose_name_plural = 'Registrations'

class ScholarshipAdmin(models.Model):
	user = models.OneToOneField(User, null=True)
	Admin = models.BooleanField(default=False)
	

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='snippets')
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
	    """
	    Use the `pygments` library to create a highlighted HTML
	    representation of the code snippet.
	    """
	    lexer = get_lexer_by_name(self.language)
	    linenos = self.linenos and 'table' or False
	    options = self.title and {'title': self.title} or {}
	    formatter = HtmlFormatter(style=self.style, linenos=linenos,
	                              full=True, **options)
	    self.highlighted = highlight(self.code, lexer, formatter)
	    super(Snippet, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)

