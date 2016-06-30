from django.shortcuts import render
import os
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
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
import dropbox
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode
from django.conf import settings

@csrf_exempt
def odk_receive(request):

    BASE_DIR = os.environ.get("BASE_DIR")
    odk_data = json.loads(request.body.decode('utf-8'))

    for data in odk_data["data"]:
        child = data["child"]
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

        if ('picture' in data) and (data['picture'] is not None) and ('url' in data['picture']):
            filename = data["picture"]["filename"]
            dropbox_upload_location = "/pictures/" + child + "/" + filename
            dbx.files_save_url(dropbox_upload_location, data["picture"]["url"])

        dropbox_upload_location = "/observations/" + child + ".txt"
        local_download_location = os.path.join(BASE_DIR, "observations", child + ".txt")
        try:
            dbx.files_download_to_file(local_download_location, dropbox_upload_location)
        except ApiError:
            pass
        with open(local_download_location, "a+") as f:
            f.write(data["submitter"] + "," + data["starttime"] + "," + data["observations"] + "\n")
        with open(local_download_location, "r") as f:
            dbx.files_upload(f.read(), dropbox_upload_location, mode=WriteMode("overwrite"))
    return HttpResponse()
