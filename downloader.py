import os
import io
import requests
from googleapiclient.http import MediaIoBaseDownload

DOWNLOAD_DIR = "downloads"

def get_photos_list(service):
    photos = []
    page_token = None

    while True:
        response = service.files().list(
            q="mimeType contains 'image/' or mimeType contains 'video/'",
            fields = "nextPageToken, files(id, name, mimeType, createdTime, thumbnailLink, webContentLink)",
            pageSize = 50,
            pageToken = page_token
        ).execute()

        photos.extend(response.get("files", []))
        page_token = response.get("nextPageToken")

        if not page_token:
            break
    return photos

def download_file(service, file_id, file_name):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, file_name)

    if os.path.exist(file_path):
        return file_path

    request = service.files().get_media(fileId = file_id)
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    with open(file_path, "wb") as f:
        f.write(buffer.getValue())
    
    return file_path

