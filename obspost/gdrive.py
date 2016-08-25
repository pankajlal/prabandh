from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from googleapiclient.http import MediaFileUpload
import urllib
from tempfile import NamedTemporaryFile
import json

#try:
#    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#except ImportError:
#    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
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
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def explain_drive_contents(child, url, name):
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()

    file_metadata = {
        'name': child,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    afile = service.files().create(body=file_metadata, fields='id').execute()
    print ('Folder ID: %s' % afile.get('id'))
    folder_id = afile.get('id')

    # items = results.get('files', [])
    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print('{0} ({1})'.format(item['name'], item['id']))

    file_metadata = {
        'name': name,
        'parents': [folder_id]
    }
    import random
    import string
    randstr = ''.join(random.choice(string.uppercase + string.digits) for _ in range(0,10))
    fname = "/tmp/" + randstr + ".jpg"
    img_file = urllib.URLopener()
    img_file.retrieve(url, fname)




    media = MediaFileUpload(name, mimetype='image/jpg')
    afile = service.files().create(body=file_metadata, media_body=media,
                                   fields='id')