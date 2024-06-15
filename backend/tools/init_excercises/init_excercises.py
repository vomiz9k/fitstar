import json
import requests

url_upload = 'http://158.160.13.5:8080/upload'
url_excercise = 'http://158.160.13.5:8080/excercise'

def init_excercises():
    with open('excercise_data/main_images.json', 'r') as f:
        j = json.load(f)

    for excercise in j:
        photo_ids = []
        for photo_path in excercise['photos']:
            photo_name = photo_path[photo_path.find('/') + 1:]
            multipart_form_data = {
                'image': (photo_name, open(f'excercise_data/image/{photo_name}', 'rb')),
            }
            response = requests.post(url_upload, files=multipart_form_data)
            if response.status_code != 200:
                print("!= 200 photo")
                return
            photo_ids.append(response.json()['id'])

        excercise_json = {
            'name': excercise['name'].replace('«', '').replace('»', ''),
            'muscles': list(set(excercise['muscle'].split(',') + excercise['additionalMuscle'].split(','))),
            'type': excercise['type'],
            'equipment': [] if excercise['equipment'] == "Отсутствует" else excercise['equipment'].split(','),
            'difficulty': excercise['difficulty'],
            'image_ids': photo_ids
        }

        response = requests.post(url_excercise, json=excercise_json)
        if response.status_code != 200:
            print ("!= 200 exc:", response )
            return

init_excercises()

