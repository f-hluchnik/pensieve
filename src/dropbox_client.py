import dropbox, os
from dotenv import load_dotenv

load_dotenv()
# dbx = dropbox.Dropbox(os.getenv('DROPBOX_ACCESS_TOKEN'))
dbx = dropbox.Dropbox(
    oauth2_refresh_token=os.getenv('DROPBOX_REFRESH_TOKEN'),
    app_key=os.getenv('APP_KEY'),
    app_secret=os.getenv('APP_SECRET')
)

def upload_file(file_path):
    # Upload file to Dropbox and get shared URL
    with open(file_path, 'rb') as f:
        file_data = f.read()
    response = dbx.files_upload(file_data, '/attachments/' + os.path.basename(file_path))
    url = dbx.sharing_create_shared_link(response.path_display).url
    return url