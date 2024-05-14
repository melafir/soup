import requests
from bs4 import BeautifulSoup,Tag
import time
import os
from pathlib import Path
from dataclasses import dataclass
import re

p =Path( os.path.abspath(__file__))

addres = "https://www.hearthpwn.com/cards?filter-set=1117&filter-type=4&display=4"

@dataclass
class Card:
    title:str
    effect:str
    img:str
    race:str|None
    tavern:int|None


def takeAllPage():
    for i in range(16):
        if i ==0:
            takePage(addres,i)
        else:
            takePage(f"{addres}&page={i}",i)
        time.sleep(10)

def takePage(s:str,page:int):
    r = requests.get(s)
    with open(f"{p.parent.joinpath(f'site/page{page}.html')}","w")as f:
        f.write(r.text)

def parsePage()->list[Card]:
    c:list[Card] = []
    for i in range(16):
        site = p.parent.joinpath(f"site/page{i}.html").as_posix()
        with open(site,"r") as f:
            soup = BeautifulSoup(f.read(),'html.parser')
            table:list[Tag] = soup.find_all('table')
            rows:list[Tag]= table[1].find_all('tr')

            for i in rows:
                rowrows = i.find_all('td')
                
                if len(rowrows)>0:
                    e:str =""
                    t:str = ""
                    r=None
                    tav=0
                    im = ""
                    cardTitle:str|None = rowrows[1].find('h3').text
                    cardEffect:Tag|None = rowrows[1].p
                    cardImg= rowrows[0].img["src"]
                    cardRace:Tag = rowrows[1].ul.find('a',href=re.compile('race'))
                    cardTavern:Tag = rowrows[1].ul.find('a',href=re.compile('tier'))
                    if cardEffect!=None:
                        e = cardEffect.text
                    if cardTitle!=None:
                        t = cardTitle
                    if cardImg!=None:
                        im = cardImg
                    if cardRace !=None:
                        r = cardRace.text
                    if cardTavern !=None:
                        tav = int(cardTavern.text)
                    c.append(Card(title=t,effect=e,img=im,race=r,tavern=tav))
    return c
def makeMd(l:list[Card]):
    for i in l:
        with open(p.parent.joinpath(f"md/bg_{i.title}.md").as_posix(),"w") as f:
            f.write(f"# {i.title}\n")
            f.write(f"- Title:  {i.title}\n")
            f.write(f"- Race:  {i.race}\n")
            f.write(f"- Tier:  {i.tavern}\n")
            f.write(f"- Effect:  {i.effect}\n")
            f.write(f"- Image:  {i.img}\n")

    
if __name__=='__main__':
    makeMd(parsePage())
