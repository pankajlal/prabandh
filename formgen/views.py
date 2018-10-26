from django.shortcuts import render
from django.template.loader import get_template
from users.models import  Learner, Faculty
# Create your views here.


def odkform(request):

    learners = Learner.objects.all()
    learner_list = []
    facilitators_list = []
    for learner in learners:
        learner_list.append(learner.user)
    facilitators = Faculty.objects.all()
    for faculty in facilitators:
        facilitators_list.append(faculty.user)
    return render(request,'observation.xml', {'children': learner_list, 'facilitators': facilitators_list},)
