import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from db_data import WikiArtistDAO as art_DAO
import pymongo


def soup_through_selenium(url):
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)
    driver.get(url)
    html = driver.page_source
    driver.close()
    return BeautifulSoup(html, "html.parser")


def scrap_from_allmusic(artist):
    soup = soup_through_selenium("https://www.allmusic.com/search/typeahead/all/" + artist)
    artists = soup.find("section", class_="artist-results")
    link = "https://www.allmusic.com" + artists.findAll("li", class_="result")[0]["data-url"] + "/related"

    soup = soup_through_selenium(link)
    print("------------------- influences -----------------------")
    influencers = soup.find("section", class_="related influencers")
    for el in influencers.findAll("a"):
        print(el.contents[0])

    print("------------------- followers -----------------------")
    followers = soup.find("section", class_="related followers")
    for el in followers.findAll("a"):
        print(el.contents[0])


def scrap_from_inflooenz(artist):
    url = 'https://inflooenz.com/?artist=' + artist
    response = requests.get(url)
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    var = soup.find("span", class_="artist")
    if var is not None:
        name = var.contents[0]
        print(name)
        if name.lower() == artist.lower():
            influencers = soup.find(id="influencers-list")
            followers = soup.find(id="followers-list")
            influencers_list = list()
            followers_list = list()

            if influencers is not None:
                for el in influencers.findAll("li", class_="item"):
                    cont = el.find('a').contents
                    if len(cont) > 0:
                        influencers_list.append(cont[0])

            if followers is not None:
                for el in followers.findAll("li", class_="item"):
                    cont = el.find('a').contents
                    if len(cont) > 0:
                        followers_list.append(cont[0])

            response.close()
            return influencers_list, followers_list
        else:
            return("different names")
    else:
        return ("artist not found")


def scrap_all_artists_influences():
    count=0
    try:
        for artist in art_DAO.find_all():
            if "inflooenz_influences" not in artist:
                count += 1
                print("\n%d: %s" %(count, artist["label_ext"]))
                res = scrap_from_inflooenz(artist["label"])
                if res == "different names":
                    artist["inflooenz_influences"] = "different names"
                    artist["inflooenz_followers"] = "different names"
                    art_DAO.replace(artist)
                    print("++++++++++ different names")
                elif  res =="artist not found":
                    artist["inflooenz_influences"] = "not found"
                    artist["inflooenz_followers"] = "not found"
                    art_DAO.replace(artist)
                    print("--------- artist not found")
                else:
                    influences, followers = res
                    print(influences)
                    print(followers)
                    artist["inflooenz_influences"] = influences
                    artist["inflooenz_followers"] = followers
                    art_DAO.replace(artist)
    except (pymongo.errors.CursorNotFound, requests.exceptions.ConnectionError):
        print('------------------- CursorNotFound Error: ' + artist['_id'])
        scrap_all_artists_influences()

scrap_all_artists_influences()

#artist = input("insert artist:")
#start = time.time()
#print(scrap_from_inflooenz(artist))
#print(time.time() - start)
