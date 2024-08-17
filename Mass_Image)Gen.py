##THIS SCRIPT IS DEVELOPED IN A COLAB ENVIROMENT

import requests
from bs4 import BeautifulSoup
import re
import time
import json
import random
import os
from concurrent.futures import ThreadPoolExecutor


class Bing_Image_Gen:
    def __init__(self,cookie_path)-> None:
        self.base_url = "https://www.bing.com"
        self.session=requests.Session()
        self.session.headers={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "Cookie": "ipv6=hit=1721963175278&t=6; _IDET=MIExp=0; MC1=GUID=00bea58841a74199a45c41d23a3d34a7&HASH=00be&LV=202407&V=4&LU=1721859376130; MS0=631dcc7a4d16468a8231585fe2ba3aea; display-culture=en-US; ak_bmsc=747409BD68CE723D6BC3E5984FA5FCAE~000000000000000000000000000000~YAAQVnIsMUiOON2QAQAAhlHR5hg2a18C84lJ5j/Qj12NotBPnfOceJH16znzKoxbUnG+ebblROHxHT04r7+7XXiMgvhBOI+8GDk2TigcRBF4p2PGMd2pBwhn8bNXKumkN7bYuqR/pGhbihZxX+y6Fa2HDjx8UIognEiKMJKJCPVMQ/QL9yzsSQU25cTpnKcKeg1x6Ba6dzhdEDYrHtb8EoQWuaqFiXVmQUKJ5YP2O/Ll5h1T/8PiYurTT8esU/+cpQdiMflhzIKpc6Qte9x10A1wsB5Boae8H49RkKQ6xJZ6VwsxOre22b9PygpgWGM7Eib76BopfR3cY6kyR8ICtZamoGppYmTebCZPL3oyJrufWWo4aHYl4cUPWI4SwLByCw==; market=IN; MSCC=NR; _clck=b8a0bg%7C2%7Cfnq%7C1%7C1666; fptctx2=H3ihr9e92IdW6yd1ZgQ9S5rgl8oOzJXlGHKxtZ4bVKotDjiG0UiwuBmfYgDIDJ3CI6GfZoKiiK0yHcL2lpuDL9rgLHSXfmW6nTyt%252b3wtY0S2aWbCXXgJsYI89Mxq9c3bNkQNTht7pR5gaNaGCLbmb%252fchjEnleNrH6%252b55WWuxxH2uVbUk9mSuGWng4MgACMFkcXkd%252bdLCNYe1ljfp%252bd2GvzB2Cb26ePzj%252fFLknCxdbHAVdWIZI53unbxdVLURpdd9tBwU8kWbu6%252f7o2FQwm5ddjDd6acBY5c%252bB2LK01unE9cTr3RefIYjEzAkjF7860DNvwcb7D9ES3VxYcqx%252fjO7tA%253d%253d; _C_Auth=; USRLOC=HS=1; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=245824CA5A6A4A4DBFA269D501DC4795&dmnchg=1; MUID=CCEFC74D4BCD43DB8CEBBB8E05ABFE20; MUIDB=CCEFC74D4BCD43DB8CEBBB8E05ABFE20; _Rwho=u=d&ts=2024-07-24; CSRFCookie=17bce7b0-beba-46f9-bc05-be48cebba8a3; SRCHUSR=DOB=20240724&T=1721859478000&POEX=W; ANON=A=2968B7E495E313911255694AFFFFFFFF&E=1e0a&W=1; NAP=V=1.9&E=1db0&C=JN7whHUS9anxmtbfABWaSU8Tfcofd4cAsIODoal3mVPlvF63vUwpOA&W=1; PPLState=1; KievRPSSecAuth=FADCBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACPinaqNkMg+qgAQU49GPwIMoW6AGMxVnDi6VDuylaJeKl6CB7zlWp2/87RMMHT8AI7YfrzYu32jOb5eHQDu+f7BTU5HPiSy2Bn9ThWiXDOVWsqdZ6B6bZaF8O9LwFLlUoHSdCn9qL9Ajtm7Y/rHcK18qwOn/2IQ0ZQMDsmuNW/OUBIaqstMJoutFKPSansCZF3QuekTWVAXULveflJT3rB80mSqSzuuJsNnr0Ut77S6By+CnVBdcvIZlpR2azJjslutWwhEZWucos+SEyvKwPHybpy0qpBFqL17UNFSIkmpzy5nEBUBlfwjyD5pulOXOFOAyjnykEek1mt1kS10xnIW8OVVDrz+t4yM0EdmW7n1S+ZpaIPYTnPwioLuM4+P7GxjfKwXHVCSrbrYRc2fd1+5rg514rrSKC7J4N3jEB0kHtMeN25U0M83oz4tXE8rBT3YlGhn/Rk1pKxarYdbqcgqxlVmGFTIgV5lUtcidSmDMRo2T6XPK9IpEJzuBy5DZSaYz8pD625rnt4EZKUb+cPfSih1X8gOnIIyS0tt74kYjIdQCaJ4BQYZi+faKQ5MwyLTVcULrh46m+ITzQHyOBZnR8dKeIUvyWJ6Z+d0KjExxmUEIT6B0yd2OmoSR2phgkLyzTHbeuyIzzMoiYw0/dKsL3efO8Xf0USUkBvrA3ONJ/00s99fMEpRo9Gzvo6Y8yk2cM5uLGBEd3GPbM5vl5t9SBnJPZ+qOKzgABpDzy0IJjOBW0jrooeEQQ7zSTpu6SzKAFAr9uKYk8UFwKUyhnDBaT/IJdlOFNK56rEjXwO3HZNkZMn5aazuUfcwZOSqgvOnE/Ek1mZVT5cksXscGJjQO5MxdoxsWrFlBhWvyXK0tR1cMjxZd7GLEl0l7IJy4vc+du1Ijy6HR3QbqpZc8R2xmbu9izLvfcvGu8E4mSDypRwYqDqfGCX/mvFVrKcKGDSo1jOW9uNa8n6JuTDGQfetcHGw4YQEyGUehQkpC9bjT7lcRQHagjvDEBHBuRTEbHPihsXdsdbPpX352mxRe4B5XkGSHnloy1YD8XZZuZQa6RyyJ7XagqsCoLZlv+dp/K5Kuh/9qeNumaTxcsaz8GbFqlAQ6EpIFQ3/xQL/vHLtoG836f7NZcDUgfRXCCeNOvVAuCOuLOOwehNG4ypuG61TKbbyLhtwLsmxAqfIURlGjuAXsGqBYZG+baqrVgR7b92V/wk2TvYbraW2mArb8YPJeJJkvZhuNd3DwCg22hzcy78jOSkA666v814F/PbE+eyE0g6dgrg/fgzutG3UOPKmtvZg8uF0W0tTgh1CEP+TpSjwYq5MUT8ItNaS9WvLxvapABSMs5ilEemDZ7JHuQHkAp6jKMIDujsdaPO9CnhX7kwCvpyNK5hTw6M116J/TrKnrZy2oqhNJ7/8BdQBJYYw0n6ep2umH1cE/HAAJh+T22i8rLD1ifXnpU2UEjN1R5i3LzTPjWr+TBMFo9cGhQH+CA8BhQPkIt/rva8gtBIDatUhWbTJfXQSgChjlMufdt0Rujs4BBgovFxAUAODyj0LzIZCiy/jnuhMtburaEstH; _U=1swPywaTZvQgH1M6dLFimI97RWt6H5xvm5M9lqtsqGQifPA5MoSMOPf_WrC-L1VsyKQ77ggMGT6fTKmZ9qE1wnDNly4WCxf6jQQ-72oHyYl61BTItAnKhCROSKeWjMcsGIxto1Pfi-o8oRr0f7rhtYz3NzxmtB7-5TwiJf3hcy9sVlSPkJYCtI6T__TTELtzbKJp2bUixcAYN6Sc8nDFjXF22AyTkHgfh1qj_L1T1Yhs; WLS=C=314a06b37b6f1f8b&N=evelyn; WLID=iDF60fn/Pn0MNHNz/6yfN6Prm9qj97JLVN8c/ObjvCjyAsvXq1RFTIpPf2Zu5onxOd2WlxGJbyNugXbsP1TkzyGCiPbhEea6uPoY08qM0qc=; _uetsid=8f18ec704a0a11ef8933d98f5ea2b3b6; _uetvid=8f18fe404a0a11ef86b5e5a8eab01b4e; _SS=SID=1ECEFEB6025B6C4625E2EA7003D56DC6&R=0&RB=0&GB=0&RG=0&RP=0; _RwBf=r=0&ilt=1&ihpd=1&ispd=0&rc=0&rb=0&gb=0&rg=0&pc=0&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=2&l=2024-07-24T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=0001-01-01T16:00:00.0000000-08:00&rwflt=2024-07-24T15:15:29.7838857-07:00&o=0&p=MSAAUTOENROLL&c=MR000T&t=8643&s=2024-07-19T20:43:29.9428245+00:00&ts=2024-07-24T22:18:04.0546603+00:00&rwred=0&wls=2&wlb=0&wle=0&ccp=2&cpt=0&lka=0&lkt=0&aad=0&TH=&W=1&mta=0&e=bqFVowhTRHbaECe7BgCj1MAOUzQFVeNOCiTvC9MfoQnRjE9kRNWNQ9Ci83D64tTbkJ5waw3QAtPwIe57G_70jA&A=2968B7E495E313911255694AFFFFFFFF; MMCASM=ID=5EB5BDE74AD0416E86965D8F4523717F; MicrosoftApplicationsTelemetryDeviceId=1872fa7f-ee3f-497d-a240-8c2201c4f375; GI_FRE_COOKIE=gi_prompt=5; _EDGE_S=SID=1ECEFEB6025B6C4625E2EA7003D56DC6&mkt=en-in&ui=en-us; SRCHHPGUSR=SRCHLANG=en&PV=15.0.0&BRW=XW&BRH=M&CW=1912&CH=958&SCW=1912&SCH=958&DPR=1.0&UTC=330&DM=1&CIBV=1.1792.0&HV=1721859628&WTS=63857456278&PRVCW=1912&PRVCH=958; _clsk=14kw5sw%7C1721859926020%7C13%7C1%7Ct.clarity.ms%2Fcollect; bm_sv=811CBAC312274795324536E8DC8F2ACE~YAAQZ3IsMQOp4OSQAQAACa3Z5hhhsWH6fgS9tIvnHSJJu/H4RgwAR09cvlr678QLpbVbQ3rU0V/9hX/hz+rWxia5XURWzbkFz1VysWKnHh72BJJ5K7Ty3jxSoPwxr1RDDtaaVZolms5A1au4aiQaenaJTqGYC0WWTYrcigQYl8Us4nPKPfg5RXOKCYL93qYymvkt9Un8TqQkiaOns+NbdeMOw6fRvI5eepnVdHSWfV/d/TQcpwY4I3qwl0XlbqnqVTfskQ==~1",
            "referrer": "https://www.bing.com/images/create/",
            "origin": "https://www.bing.com",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
            "x-forwarded-for": f"13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
        }
        for cookie in json.load(open(cookie_path)):
            self.session.cookies.set(cookie["name"],cookie["value"])
            self.quiet= False

    def start_generation_sequence(self, url_encoded_prompt, name):
        payload= "q="+url_encoded_prompt+f"&rt=3&FORM=GENCRE"
        url=f"{self.base_url}/images/create?q={url_encoded_prompt}&rt=3&FORM=GENCRE"
        response=self.session.post(url,allow_redirects=False, data=payload, timeout= 200)
        if response.status_code!=302:
            print(name)
            print("Error while generating. Error Code ="+ str(response.status_code))
            return 1
        id='1-'+response.headers["X-Eventid"]
        return id

    def get_download_links(self, url, name):
        start_wait = time.time()
        while True:
            if int(time.time() - start_wait) > 100:
                print("timeout:",name)
                print(response.text)
                return
            response = self.session.get(url)
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                element = soup.find(id="mmComponent_images_1")
                x = [i.get('href').split('thId=')[-1].split('&')[0] for i in element.find_all('a') if 'images' in str(i.get('href'))]
                if len(x) < 1 :
                    time.sleep(1)
                    continue
                else:
                    break
            except:
                time.sleep(1)
                continue
        return x[:4]

    def Generate(self,prompt: str, name: str)-> list:
        url_encoded_prompt = requests.utils.quote(prompt)
        id=self.start_generation_sequence(url_encoded_prompt, name)
        if id != 1:
            new_url=f"https://www.bing.com/images/create/{url_encoded_prompt}/{id}?FORM=GUH2CR"
            links = self.get_download_links(new_url, name)
            for i in links:
                self.save_to_drive(i)
        else:
            pass

    def save_to_drive(self, id):
        name = id+'.jpg'
        path = '/content/drive/MyDrive/Unchecked/'+name
        response = requests.get(f"https://th.bing.com/th/id/{id}?pid=ImgGn")
        if response.status_code == 200:
            with open( path, 'wb') as f:
                f.write(response.content)

ethan = Bing_Image_Gen("/content/drive/MyDrive/Cookies/ethan.json")
mason = Bing_Image_Gen("/content/drive/MyDrive/Cookies/mason.json")
amelia = Bing_Image_Gen("/content/drive/MyDrive/Cookies/amelia.json")
alexander = Bing_Image_Gen("/content/drive/MyDrive/Cookies/alexander.json")
henry = Bing_Image_Gen("/content/drive/MyDrive/Cookies/henry.json")
mia = Bing_Image_Gen("/content/drive/MyDrive/Cookies/mia.json")
evelyn = Bing_Image_Gen("/content/drive/MyDrive/Cookies/evelyn.json")
sanu = Bing_Image_Gen("/content/drive/MyDrive/Cookies/sanu.json")
shreyash = Bing_Image_Gen("/content/drive/MyDrive/Cookies/shreyash.json")
arya = Bing_Image_Gen("/content/drive/MyDrive/Cookies/arya.json")

def task(session, prompt):
    session, name = session
    session.Generate(prompt, name)

def run_tasks(sessions, prompt):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(task, session, prompt) for session in sessions]
        for future in futures:
            future.add_done_callback(lambda x: None)
prompts = open('/content/drive/MyDrive/Cookies/prompts.txt','r').read().split('\n')
bots = [[(ethan,'ethan'), (mason,'mason')], [(amelia, 'amelia'), (alexander, 'alexander')], [(henry, 'henry'), (mia, 'mia')], [(evelyn, 'evelyn'), (sanu, 'sanu')], [(shreyash, 'shreyash'), (arya, 'arya')]]
for i in range(len(prompts)):
    print(prompts[i],f'{i}/{len(prompts)}')
    used_bots = [pair[i%2] for pair in bots]
    run_tasks(used_bots, prompts[i])
