import requests
from bs4 import BeautifulSoup
import pprint

all_links = []
all_subtext = []
for n in range(1, 6):
    response = requests.get(f'https://news.ycombinator.com/news?p={n}')
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select('.titleline > a')
    subtext = soup.select('.subtext')
    all_links = all_links + links
    all_subtext = all_subtext + subtext


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for index, _ in enumerate(links):
        title = links[index].getText()
        href = links[index].get('href', None)
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(all_links, all_subtext))
