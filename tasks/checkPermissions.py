from main.models import Settings
from django.utils import timezone

def isAlow(request):
    if request.user.is_anonymous==True or (request.user.is_specialist==False and request.user.is_superuser==False):
        try:
            s=Settings.objects.all()
            now=timezone.now()
            if (s[0].start_date!=None and s[0].start_date>now) or (s[0].end_date!=None and s[0].end_date<now):
                return False
        except:
            pass
    return True