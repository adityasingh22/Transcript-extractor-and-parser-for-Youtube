import json
import re
import requests
import logging
from os import read, write

logging.getLogger().setLevel(logging.INFO)


def getUrl():
    video_id = input("Enter the video ID ")
    expire = input("Enter the expire ")
    signature = input("Enter the signature ")
    lang = input("Enter the language to convert to ")
    getRequest(video_id, expire, signature, lang)

def checkUrl(url):
        response=requests.get(url=url)
        if (response.status_code == 200 and len(response.text)!=0):
            return response.json()
        url=re.sub(r'(\&lang=en)', r'\1-US', url)
        response=requests.get(url=url)
        if (response.status_code == 200 and len(response.text)!=0):
            return response.json()
        url+='&caps=asr'
        url=re.sub(r'(\&sparams=ip,ipbits,expire,v,)', r'\1caps,', url)
        response=requests.get(url=url)
        if (response.status_code == 200 and len(response.text)!=0):
            return response.json()
        url=re.sub(r'(?<=lang=en)-US', r'', url)
        response=requests.get(url=url)
        if (response.status_code == 200 and len(response.text)!=0):
            return response.json()
        return None

def getRequest(video_id, expire, signature, lang):
    logging.info(
        "Received url parameters, fetching URL in language {0}....".format(lang))

    url = "https://www.youtube.com/api/timedtext?v={video_id}&xoaf=5&ip=0.0.0.0&ipbits=0&expire={expire}&sparams=ip,ipbits,expire,v,xoaf&signature={signature}&key=yt8&lang=en&fmt=json3&tlang={lang}".format(
        video_id=video_id, expire=expire, signature=signature, lang=lang)

    logging.info("Fetching response in en....")

    url_en = "https://www.youtube.com/api/timedtext?v={video_id}&xoaf=5&ip=0.0.0.0&ipbits=0&expire={expire}&sparams=ip,ipbits,expire,v,xoaf&signature={signature}&key=yt8&lang=en&fmt=json3".format(
        video_id=video_id, expire=expire, signature=signature)

    try:
        translated_json=checkUrl(url)
        en_json=checkUrl(url_en)
        if translated_json is None or en_json is None:
            logging.error("Error in json")
    except:
        logging.error("Error in the URL specified. Please check the URL")
        return

    logging.info("Mapping translated text and en text")

    try:
        f_2 = open('mapped_transcript.txt', 'w')
        i = 0
        for translation in translated_json['events']:
            f_2.write(translation['segs'][0]['utf8'])
            f_2.write("|")
            f_2.write(en_json['events'][i]['segs'][0]['utf8'])
            f_2.write("\n")
            i += 1
    except:
        logging.error("Error in reading json")
        return
    else:
        logging.info("Texts are mapped")
    finally:
        f_2.close()

if __name__ == '__main__':
    getUrl()