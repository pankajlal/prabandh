from django.shortcuts import render
import os
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import logging
from django.conf import settings
#from common.utils import logger
#{
# "token":"",
# "content":"record",
# "formId":"build_BeMe-Observations_1466792215",
# "formVersion":"",
# "data":[
#    {"*meta-instance-id*":"uuid:60754793-2619-4bba-8a33-49e66684a050",
#     "*meta-model-version*":null,
#     "*meta-ui-version*":null,
#     "*meta-submission-date*":"2016-06-25T09:18:02.987Z",
#     "*meta-is-complete*":true,
#     "*meta-date-marked-as-complete*":"2016-06-25T09:18:02.987Z",
#     "instanceID":"uuid:60754793-2619-4bba-8a33-49e66684a050",
#     "picture":{
#        "filename":"1466834286870.jpg",
#        "type":"image/jpeg",
#        "url":"https://beme-odk-collect.appspot.com/view/binaryData?blobKey=build_BeMe-Observations_1466792215%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2Fdata%5B%40key%3Duuid%3A60754793-2619-4bba-8a33-49e66684a050%5D%2Fpicture"
#      },
#      "observations":"Enjoyed coffee",
#      "child":"abhimanyu",
#      "submitter":"parent",
#      "starttime":"2016-06-25T01:36:28.646Z"
#     }
#   ]
# }

FORM_ID = "build_BeMe-Observations_1466792215"

DROPBOX_ACCESS_TOKEN = os.environ.get("DROPBOX_AUTH_TOKEN")
FILE_BASE_PATH = ""
import json
from datetime import datetime
from obspost.gsheets import append_gsheets
from .models import Observation, ChildSheet,ObservedChild
from .gdrive import upload_file
from users.models import Learner
from django.utils.dateparse import parse_datetime
import logging
logger = logging.getLogger(__name__)

BEME_SHEET_ID = '1mKo5yejjD0J9gfivqlSbWw6NJchGMFFs5T2FbgbzzP4'
BEME_FOLDER_ID = '0B2W9xFXyMLWyN1lRaTYtaVhrYzQ'

def get_children_upload_specs(children):

    learner_upload_specs = []

    for child in children:
        cs = ChildSheet.objects.filter(learner__user__username = child).first()
        if cs is not None:
            user = cs.learner.user
            sheet_id = cs.sheetcode
            if cs.foldercode != 'unknown':
                folder_id = cs.foldercode
            else:
                folder_id = BEME_FOLDER_ID
        else:
            user = None
            sheet_id = BEME_SHEET_ID
            folder_id = BEME_FOLDER_ID

        learner_upload_specs.append({'user': user, 'sheet_id': sheet_id, 'folder_id': folder_id})

    return learner_upload_specs

@csrf_exempt
def odk_receive(request):
    logger.info(request)
    def get_url(data):
        if ('picture' in data) and (data['picture'] is not None) and ('url' in data['picture']):
            return data["picture"]["url"]
        else:
            return None

  #  BASE_DIR = os.environ.get("BASE_DIR")
    odk_data = json.loads(request.body.decode('utf-8'))
    now = datetime.now().strftime("%Y%m%d_%H%M")
    #A submission could consist of multiple form data. Iterate over the whole
    for data in odk_data["data"]:

        children = data.get("child")
        learner_uploads = get_children_upload_specs(children)

        #get all the folders in which this image should show
        folder_ids = []
        for learner in learner_uploads:
            for learner in learner_uploads:
                folder_ids.append(learner['folder_id'])

        instance_id = data.get("instanceID")
        observation = data.get("observation")
        submitter = data.get("username")

        picture_time = data.get("starttime")
        time_now = datetime.now().strftime("%d %b %Y %I:%M %p")
        url = get_url(data)


        if Observation.objects.filter(instance_id = instance_id).first():
            logger.info("This post has already been logged. So not logging again")
        else:
            if ('picture' in data) and (data['picture'] is not None) and ('url' in data['picture']):
                logger.info("picture found, appending the url")
                if observation:
                    name = observation
                else:
                    name = data['picture']['filename']			
                file_id = upload_file(folder_ids, url=data['picture']['url'], file_name=name)
                if file_id:
                    content = 'https://drive.google.com/open?id=%s' % (file_id)
                else:
                    content = ''
                for learner in learner_uploads:
                    append_gsheets(learner['sheet_id'], [picture_time, learner['user'].username, submitter, time_now
                                                         observation, content])
            else:
                logger.error("no picture in the post. appending without logger")
                for learner in learner_uploads:
                    append_gsheets(learner['sheet_id'], [picture_time, learner['user'].username, submitter, time_now
                                                         observation, ''])

            o = Observation(instance_id=instance_id,
                            submission_date=datetime.now(),
                            observation=observation,
                            submitter=submitter
                            )
            o.save()
            for learner in learner_uploads:
                observedchild = ObservedChild(observation = o, learner = learner['user'].learner)
                observedchild.save()

    return HttpResponse()
