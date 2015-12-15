from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from snippets.models import Snippet
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
            print('here')
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

def AdminPortal(request):
    return render(request, 'AdminPortal.html')







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

# class RegistrationSingleViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     This viewset automatically provides `list` and `detail` actions for a single Registration
#     """
#     print('2')
#     queryset = Registrations.objects.all()
#     print(queryset)
#     serializer_class = RegistrationSerializer
#     print('2.2')
#     permission_classes = (IsScholarshipAdmin)
#     print('2.3')



@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

