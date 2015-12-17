from django.contrib.auth.models import User
from django.shortcuts import render, redirect, render_to_response
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.db.models import Q

from snippets.models import Snippet, Registrations, ScholarshipAdmin
from snippets.serializers import SnippetSerializer, UserSerializer, RegistrationSerializer
from snippets.permissions import IsOwnerOrReadOnly, IsScholarshipAdmin
from snippets.models import Registrations
from snippets.forms import RegistrationForm

from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.decorators import detail_route
from rest_framework import viewsets

import datetime
import requests
import json

def contains_digits(s):
    return any(char.isdigit() for char in s)

def Homepage(request):
    return render(request, 'Homepage.html')

def Application(request):
    date = datetime.date.today()
    validForm = True
    AllErrors = []

    if 'submit' in request.POST:
        AppForm = RegistrationForm(request.POST, initial={
                                    'registration_day':date.day,
                                    'registration_month':date.month,
                                    'registration_year':date.year,
                                    })


        if AppForm.is_valid():
            if (contains_digits(AppForm.data['firstName'])):
                AllErrors.append('Invalid First Name')
                validForm = False

            if (contains_digits(AppForm.data['lastName'])):
                AllErrors.append('Invalid Last Name')
                validForm = False

            try:
                validate_email(AppForm.data['emailaddress'])
            except Exception as e:
                AllErrors.append('Invalid Email')
                validForm = False

            if (AppForm.data['studentNumber'].isdigit() == False): 
                AllErrors.append('Invalid Student Number')
                validForm = False

            try:
                float(AppForm.data['cumGpa'])
            except Exception as e:
                validForm = False
                AllErrors.append('Invalid Cumulative GPA')


            if (AppForm.data['numCredits'].isdigit() == False): 
                AllErrors.append('Invalid Number of Credits')
                validForm = False

            if(AppForm.data['cumGpa'] < 3.2):
                AllErrors.append('GPA is too low')
                validForm = False

            if(AppForm.data['numCredits'] < 12):
                AllErrors.append('Number of credits is too low')
                validForm = False

            if(AppForm.data['dob_year'] < 1992):
                AllErrors.append('Too Old')
                validForm = False
            try:
                Registrations.objects.get(studentNumber=AppForm.data['studentNumber'])
                AllErrors = []
                AllErrors.append('Student Number is Already Registered')
                validForm = False
            except Exception as e:
                print('that registration is good yo')
                
            if (validForm == False):
                return render(request, 'Application.html', {'AppForm':AppForm, 'ERRORS':AllErrors})

            url = 'http://localhost:8000/api/registrations/'
            payload = AppForm.data
            r = requests.post(url, data=payload, auth=('ScholarshipAdmin', 'pass123'))

            return render(request, 'confirmation.html')


    else:
        AppForm = RegistrationForm(initial={
                                    'registration_day':date.day,
                                    'registration_month':date.month,
                                    'registration_year':date.year,
                                    })
        

    return render(request, 'Application.html', {'AppForm':AppForm})


def AdminLogin(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('AdminLogin.html', c)

def AdminAuthorization(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:

        isAdmin = ScholarshipAdmin.objects.get(user=user)
        if (isAdmin.Admin == True):
            return HttpResponseRedirect('/AdminPortal')
    else:
        return render_to_response("invalid.html")

def AdminPortal(request):
    if (request.user.is_anonymous()):
        return HttpResponseRedirect('/')

    isAdmin = ScholarshipAdmin.objects.get(user=request.user)

    url = 'http://localhost:8000/api/registrations/'
    r = requests.get(url, auth=('ScholarshipAdmin', 'pass123'))
    applicants = r.json() 

    if (isAdmin.Admin == True):                    
        return render(request, 'AdminPortal.html', {'applicants':applicants})
    else:
        return HttpResponseRedirect('/')

def SelectWinner(request, post_id):
    if (request.user.is_anonymous()):
        return HttpResponseRedirect('/')

    winner = Registrations.objects.get(studentNumber = post_id)
    winner.winner = True

    return redirect('snippets.views.AdminPortal')

    


############ API #################
class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegistrationListViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Registrations.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (IsScholarshipAdmin,)


class WinnerSelection(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    matchFound = False
    #checking to see if there is a single person with highest gpa
    queryset = Registrations.objects.all().filter(winner=True)
    if (queryset.count() == 1):
        matchFound = True


    if(matchFound == False):
        queryset = Registrations.objects.all().order_by('-cumGpa')
        if (queryset.count() == 1):
            queryset = Registrations.objects.all()
            matchFound = True

        #check for highest cum gpa
        if (queryset[0].cumGpa == queryset[1].cumGpa):
            matchFound = False
        else:
            queryset = queryset.filter(studentNumber = queryset[0].studentNumber)
            matchFound = True

    #check for highest current gpa
    if(matchFound == False):
        queryset = Registrations.objects.all().order_by('-cumGpa')
        if(queryset[0].currGpa == queryset[1].currGpa):
            matchFound = False
        else:
            queryset = queryset.filter(studentNumber = queryset[0].studentNumber)
            matchFound = True

    #checking for only 1 Junior
    if(matchFound == False):
        queryset = Registrations.objects.filter(collegeStatus = 'J')
        if(queryset.count() == 1):
            matchFound = True
        else:
            matchFound = False
            
    #checking for only 1 female
    if(matchFound == False):
        queryset = Registrations.objects.filter(gender = 'F')

        if(queryset.count() == 1):
            matchFound = True
        else:
            matchFound = False

    #2 youngest students
    if(matchFound == False):
        queryset = Registrations.objects.all().order_by('-dob_year')
        queryset = queryset.filter(dob_year = queryset[0].dob_year)
        queryset = queryset.order_by('-dob_month')
        queryset = queryset.filter(Q(studentNumber = queryset[0].studentNumber) | Q(studentNumber = queryset[1].studentNumber))  
        matchFound = True

    serializer_class = RegistrationSerializer
    permission_classes = (IsScholarshipAdmin,)



@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

