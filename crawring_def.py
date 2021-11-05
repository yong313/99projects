import requests
from bs4 import BeautifulSoup

def crawring_embedUrl(link):
    youtube_url = requests.get(link)
    soup = BeautifulSoup(youtube_url.text, 'html.parser')
    div_find = soup.find('div',id='watch7-content')
    embedUrl = div_find.find('link',itemprop='embedUrl')['href']
    return embedUrl
def crawring_thumbnailUrl(link):
    youtube_url = requests.get(link)
    soup = BeautifulSoup(youtube_url.text, 'html.parser')
    div_find = soup.find('div',id='watch7-content')
    thumbnailUrl = div_find.find('link',itemprop='thumbnailUrl')['href']
    return thumbnailUrl
def crawring_subject(link):
    youtube_url = requests.get(link)
    soup = BeautifulSoup(youtube_url.text, 'html.parser')
    div_find = soup.find('div',id='watch7-content')
    subject = div_find.find('meta',itemprop='name')['content']
    return subject

# def cra