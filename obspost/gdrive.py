from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from googleapiclient.http import MediaFileUpload
import urllib.request as urllib
import random
import string
import os
import requests
import shutil
import logging

logger = logging.getLogger(__name__)

flags = None
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = '/home/beme/client_secret.json'
#CLIENT_SECRET_FILE = '/home/beme/drive-python-quickstart.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials(flags=None):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        #if flags:
        credentials = tools.run_flow(flow, store, flags)
        #else: # Needed only for compatibility with Python 2.6
        #    credentials = tools.run(flow, store)
    return credentials

def upload_file(folder_id, url, file_name):
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    #Create a temporary file
    randstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(0,10))
    fname = "/tmp/" + randstr + ".jpg"
    #Download the file at url into the temporary file
    r = requests.get(url, stream = True)
    logger.info("URL is %s"%url)
    logger.info("status code is %s"%str(r.status_code))
    if r.status_code == 200:
        logger.info("downloaded the picture from %s"%url)
        with open(fname, 'wb') as f:
            r.raw_decode_content = True
            shutil.copyfileobj(r.raw, f)
      
#    img_file = urllib.URLopener()
#    img_file.retrieve(url, fname)

        #Create the MediaFileUpload Object
        media = MediaFileUpload(fname, mimetype='image/jpg')

        #Obtain credentials for upload of file
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)

        file_metadata = {
            'file_name': file_name,
            'parents': [folder_id]
        }

        # Execute the upload
        afile = service.files().create(body=file_metadata, media_body=media,
                                       fields='id').execute()

        file_id = afile.get('id')
        file_update_metadata = {
            'title': file_name
        }
        v2service = discovery.build('drive', 'v2', http=http)
        updated_file = v2service.files().patch(fileId=file_id, body=file_update_metadata, fields='title').execute()

        #Return the id of the created file

        os.remove(fname)
        return file_id
    else:
        logger.error("The file was not created")
        return None
