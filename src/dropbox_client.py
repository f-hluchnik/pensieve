import dropbox, os, shortuuid
from dotenv import load_dotenv

load_dotenv()
dbx = dropbox.Dropbox(
    oauth2_refresh_token=os.getenv('DROPBOX_REFRESH_TOKEN'),
    app_key=os.getenv('APP_KEY'),
    app_secret=os.getenv('APP_SECRET')
)

def upload_file(file_path):
    """
    upload_file ... Function will upload file to dropbox and return url of that file.
    """
    with open(file_path, 'rb') as f:
        file_data = f.read()
    file_name = shortuuid.uuid()
    file_extension = os.path.splitext(file_path)[1]
    dest_name = file_name + file_extension
    response = dbx.files_upload(file_data, '/attachments/' + os.path.basename(dest_name))
    url = dbx.sharing_create_shared_link(response.path_display).url
    return url