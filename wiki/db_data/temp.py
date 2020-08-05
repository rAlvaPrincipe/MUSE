from db_data import DAO_temp
from db_data import WikiArtistDAO as art_DAO

for musician in DAO_temp.find_all():
    artist = art_DAO.find_by_id(musician["_id"])
    if artist is not None:
        artist["inflooenz_influences"] = musician["inflooenz_influences"]
        artist["inflooenz_followers"] = musician["inflooenz_followers"]
        art_DAO.replace(artist)
    else:
        print("None: " + musician["_id"])
