# from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TeamSerializer as ser

from team.models import Teams

class test_api(APIView):
    def get(self,request):
        ls=Teams.objects.all()
        ls=ser(ls,many=True)
        return Response({"test":ls.data})
# Create your views here.
