import dropbox, os, shortuuid
from dotenv import load_dotenv

class DropboxClient():
    def __init__(self):
        load_dotenv()
        self.dbx = dropbox.Dropbox(
            oauth2_refresh_token=os.getenv('DROPBOX_REFRESH_TOKEN'),
            app_key=os.getenv('APP_KEY'),
            app_secret=os.getenv('APP_SECRET')
        )

    def upload_file(self, file_path):
        """
        upload_file ... Function uploads file to Dropbox and returns url of the uploaded file.
        """
        with open(file_path, 'rb') as f:
            file_data = f.read()
        name = shortuuid.uuid()
        extension = os.path.splitext(file_path)[1]
        file_name = name + extension
        url = ""
        try:
            response = self.dbx.files_upload(file_data, '/attachments/' + os.path.basename(file_name))
        except Exception as e:
            raise ValueError(f"Failed to upload file: {e}")

        try:        
            shared_link = self.dbx.sharing_create_shared_link(response.path_display)
            url = shared_link.url
        except Exception as e:
            raise ValueError(f"Failed to create shared link: {e}")
        return url