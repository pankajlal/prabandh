from django.shortcuts import render

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

DROPBOX_ACCESS_TOKEN = 'INf6UK08gzAAAAAAAAAAB3la9RwEaDqEf9Uh3AgSU3e9oZzw_v8NMgJV_sbvLxsR'
FILE_BASE_PATH = ""
import json
import dropbox

from obspost.models import Observation

@csrf_exempt
def odk_receive(request):
    odk_data = json.loads(request.body.decode('utf-8'))
    with open('data.txt', 'w') as outfile:
        json.dump(odk_data, outfile)
    if odk_data["formId"] != FORM_ID:
        #Just ignore the request as we can handle only the very specific form for observation as of now.
        #Later we can build some capability to handle multiple types of forms here.
        return HttpResponse()

    for data in odk_data["data"]:
        child = data["child"]
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

        if data["picture"] != '':
            filename = data["picture"]["filename"]
            upload_location = "/" + child + "/" + filename
            dbx.files_upload(data["picture"]["bytes"], upload_location)

        upload_location = "/" + child + "/observations.txt"
        dbx.files_upload("Submitted By: " + data["submitter"] + " at: " + data["starttime"] + " : " + data["observations"],upload_location, mode="add")

    return HttpResponse()
