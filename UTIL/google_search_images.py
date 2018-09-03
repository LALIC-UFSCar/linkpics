from bs4 import BeautifulSoup
import requests
import re
import urllib
import os
from urllib.request import urlopen
import urllib.request as r
import cv2

def get_soup(url, header):
    return BeautifulSoup(urlopen(r.Request(url, headers=header)))


def get_images(query):
    #image_type = "Action"
    # you can change the query for the image  here
    query = query.split()
    query = '+'.join(query)
    url = "https://www.google.com.br/search?hl=pt-pt&site=imghp&tbm=isch&source=hp&biw=1366&bih=652&q=" + query + "&oq=" + query + "&gs_l=img.3..35i39k1l2j0l8.2758.3652.0.3918.6.6.0.0.0.0.162.658.0j5.5.0....0...1.1.64.img..1.5.657.0.9sV876WDKM4"
    header = {'User-Agent': 'Mozilla/5.0'}
    soup = get_soup(url, header)
    images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
    #print images
    DIR = ""
    DIR = "/data/alinhador/faceDB/images_crawled/" + query.replace("+", "_") + "/"
    #DIR_back = "/data/alinhador/faceDB/images_crawled/" + query.replace("+", "_") + "/"
    if not os.path.exists(DIR):  # se as imagens ainda não foram coletadas
        os.makedirs(DIR)
        for img in images:
            raw_img = urlopen(img).read()
            #add the directory for your image here
            cntr = len([i for i in os.listdir(DIR)]) + 1
            f = open(DIR + query.replace("+", "_") + "_" + str(cntr) + ".jpg", 'wb')
            
            f.write(raw_img)
            f.close()

    return DIR