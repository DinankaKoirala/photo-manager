import os
import requests

DOWNLOAD_DIR = "downloads"

def get_photos_list(creds):
    photos = []
    page_token = None
    headers = {"Authorization": f"Bearer {creds.token}"}

    while True:
        params = {"pageSize": 50}
        if page_token:
            params["pageToken"] = page_token

        response = requests.get(
            "https://photoslibrary.googleapis.com/v1/mediaItems",
            headers=headers,
            params=params
        )

        data = response.json()
        print("Status code:", response.status_code)
        print("API response:", data)
        print("Token:", creds.token[:20], "...")
        items = data.get("mediaItems", [])
        photos.extend(items)
        page_token = data.get("nextPageToken")

        if not page_token:
            break

    return photos 


def download_file(creds, base_url, file_name):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, file_name)

    if os.path.exists(file_path):
        return file_path
    
    headers = {"Authorization": f"Bearer {creds.token}"}
    download_url = base_url + "=d"
    response = requests.get(download_url, headers=headers)

    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path