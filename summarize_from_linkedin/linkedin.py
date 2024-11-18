import os
import requests
from dotenv import load_dotenv
load_dotenv()
gist_response = requests.get("https://gist.githubusercontent.com/yusufcanekin/08d4a94d03b7d93676971eec1bd42095/raw/17a06a12bb90f81c51c71d1df967f5d983219972/yusuf-can-ekin.json")

def scrape_linkedin_profile(linkedin_profile_url:str, mock: bool = True):
    if mock:
        response = requests.get(
            "https://gist.githubusercontent.com/yusufcanekin/08d4a94d03b7d93676971eec1bd42095/raw/17a06a12bb90f81c51c71d1df967f5d983219972/yusuf-can-ekin.json"
        )
    else:
        api_key = 's3yUPd73iBC8ry8GbpqjCQ'
        headers = {'Authorization': 'Bearer ' + api_key}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        params = {
            'url': linkedin_profile_url
        }
        response = requests.get(api_endpoint,
                                params=params,
                                headers=headers)

    data = response.json()
    data = {
        k:v
        for k, v in data.items()
        if v not in ([], ""," ", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    return data

