import os
import json
import requests
from urllib.parse import urlparse 
from os.path import splitext


better_discord_media_location = (os.getenv('APPDATA')) + "\BetterDiscord\plugins\FavoriteMedia.config.json"

with open(better_discord_media_location, 'r') as f:
    media_json = json.loads(f.read())


try:
    os.mkdir('videos')
except:
    pass

try:
    os.mkdir('images')
except:
    pass


if "backup_data.json" in os.listdir():
    with open("backup_data.json", 'r') as f:
        backup_data_urls = json.loads(f.read())
        backup_data_urls = backup_data_urls['urls']

else:
    backup_data_urls = []


if 'video' in media_json:

    file_numu = 0
    
    for video in media_json['video']['medias']:
        if video['url'] not in backup_data_urls:
            backup_data_urls.append(video['url'])
            r = requests.get(video['url'])
            path = urlparse(video['url']).path
            ext = splitext(path)[1]
            file_name = f"videos/{video['name']}{ext}"

            if f"{video['name']}{ext}" in os.listdir("videos"):
                file_name = f"videos/{video['name']}({file_numu}){ext}"
                file_numu += 1

            with open(file_name, 'wb') as f:
                f.write(r.content)

if 'image' in media_json:

    file_numu = 0

    for image in media_json['image']['medias']:
        if image['url'] not in backup_data_urls:
            backup_data_urls.append(image['url'])
            r = requests.get(image['url'])
            path = urlparse(image['url']).path
            ext = splitext(path)[1]
            file_name = f"images/{image['name']}{ext}"

            if f"{image['name']}{ext}" in os.listdir("images"):
                file_name = f"images/{image['name']}({file_numu}){ext}"
                file_numu += 1

            with open(file_name, 'wb') as f:
                f.write(r.content)

backup_data_urls = {'urls': backup_data_urls}

with open("backup_data.json", 'w') as f:
    f.write(json.dumps(backup_data_urls))
