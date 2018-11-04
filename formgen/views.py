from django.shortcuts import render
from django.template.loader import get_template
from users.models import  Learner, Faculty
from datetime import datetime
import random
# Create your views here.


def odkform(request):

    learners = Learner.objects.all()
    learner_list = []
    facilitators_list = []
    for learner in learners:
        learner_list.append({'username': learner.user, 'first_name': learner.user.first_name, 'last_name':
            learner.user.last_name})
    facilitators = Faculty.objects.all()
    for faculty in facilitators:
        facilitators_list.append(faculty.user)
    timenow = datetime.now()
    version = timenow.strftime("%Y%j") + str(random.choice(range(100))).zfill(3)
    return render(request,'observations_multi_select.xml', {'children': learner_list, 'version': version})
