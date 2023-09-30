import random 
from typing import Dict, List
import requests
from bs4 import BeautifulSoup
import re
import time
import json

bing="https://www.bing.com"
FORWARDED_IP = f"13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "referrer": "https://www.bing.com/images/create/",
    "origin": "https://www.bing.com",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
    "x-forwarded-for": FORWARDED_IP,
}

class Image_Gen:
    def __init__(self,all_cookies: List[Dict])-> None:
        self.session=requests.Session()
        self.session.headers=HEADERS
        for cookie in all_cookies:
            self.session.cookies.set(cookie["name"],cookie["value"])
            self.quiet= False
    def Generate(self,prompt: str)-> list:
        url_encoded_prompt = requests.utils.quote(prompt)
        payload= "q="+url_encoded_prompt+"&qs=ds"
        urls=[f"{bing}/images/create?q={url_encoded_prompt}&rt={rt}&FORM=GENCRE" for rt in [4, 3]]
        for i in urls:
            response=self.session.post(i,allow_redirects=False, data=payload, timeout= 200)
            if response.status_code==302:
                break
            else:
                print("Error while generating. Error Code ="+ response.status_code)
        id=response.headers["Location"].split("id=")[-1]
        new_url=f"https://www.bing.com/images/create/async/results/{id}?q={url_encoded_prompt}"
        start_wait = time.time()
        while True:
            if int(time.time() - start_wait) > 200:
                print("timeout")
            response = self.session.get(new_url)
            if response.status_code != 200 or not response.text or response.text.find("errorMessage") != -1:
                time.sleep(1)
                continue
            else:
                break
        img_tags = BeautifulSoup(response.text, 'html.parser').find_all('img',{'class': 'mimg'})
        links=[]
        for img in img_tags:
            l=img.get('src')
            l=re.sub(r'w=\d+&h=\d+&c=\d+&r=\d+&o=\d+&', '', l)
            links.append(l)
        
        return links
