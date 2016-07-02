from django.shortcuts import render

# Create your views here.
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

from isbntools import app
from .models import Isbn, Author
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def isbn_post(request):
    odk_data = json.loads(request.body.decode('utf-8'))

    isbn_details = odk_data.get('data')
    for item in isbn_details:
        isbn_no = item.get('isbn')
        meta_dict = app.meta(isbn_no)
        if meta_dict:
            if meta_dict.get('Title'):
                try:
                    isbn = Isbn.objects.get(code=isbn_no)
                except ObjectDoesNotExist:
                    isbn = Isbn(code=isbn_no,
                            title=meta_dict.get('Title'),
                            publisher=meta_dict.get('Publisher'),
                            year=date(2001, 1, 1)
                            )
                    isbn.save()
                for a in meta_dict.get('Authors'):
                    try:
                        author = Author.objects.get(name=a)
                    except ObjectDoesNotExist:
                        author = Author.objects.create(name=a)
                    isbn.authors.add(author)
    return HttpResponse()



