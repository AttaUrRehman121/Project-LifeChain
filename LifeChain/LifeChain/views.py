from django.shortcuts import redirect, render , HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.db import IntegrityError
from django.http import Http404



