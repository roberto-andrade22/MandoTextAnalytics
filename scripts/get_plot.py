import requests
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import re

base_url = "https://starwars.fandom.com/"

def get_season_links(season_url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' }
    page_season = requests.get(season_url, headers=headers).content
    soup = BeautifulSoup(page_season, 'html.parser')
    table = soup.find('table',{'id':'prettytable'})

    urls = []

    for row in table.find_all('tr')[1:]:
        tds = row.find_all('td')
        link = tds[2].find('a')
        urls.append(link.get('href'))
    
    return(urls)

def between(cur, end):
    while cur and cur != end:
        if isinstance(cur, NavigableString):
            text = cur.strip()
            if len(text):
                yield text
        cur = cur.next_element


def get_episode_plot(episode_url):
    to_scrape = base_url + episode_url
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' }
    episode = requests.get(to_scrape, headers = headers).content
    soup = BeautifulSoup(episode, 'html.parser')
    if soup.find('span', id= 'Development'):
        txt = ' '.join(text for text in between(soup.find('span', id='Plot_summary').next_sibling,
                                    soup.find('span', id='Development')))
    elif soup.find('span',id = 'Continuity'):
        txt = ' '.join(text for text in between(soup.find('span', id='Plot_summary').next_sibling,
                                    soup.find('span', id='Continuity')))
    else:
        txt = ' '.join(text for text in between(soup.find('span', id='Plot_summary').next_sibling,
                                        soup.find('span', id='Credits')))
    txt = re.sub('(\[ ])',"",txt)
    return(txt)    


def get_season_plot(url_season):
    season_links = get_season_links(url_season)
    return([get_episode_plot(ep) for ep in season_links])


season_one = base_url + "wiki/The_Mandalorian_Season_One"
season_two = base_url + "wiki/The_Mandalorian_Season_Two"
book_of_boba_fett = base_url + "wiki/The_Book_of_Boba_Fett"

season_one_episodes = get_season_plot(season_one)
season_two_episodes = get_season_plot(season_two)
boba_fett_episodes = get_episode_plot(book_of_boba_fett)