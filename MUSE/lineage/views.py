from django.shortcuts import render
from db_data import graphDAO as graph_DAO

def get_nodes(id, inflooenz, patterns, classificator):
    influencers = set()
    followers = set()

    if inflooenz == "true":
        for record in  graph_DAO.connections_from(id, "inflooenz_by"):
            influencers.add((record["b"]["URL"], record["b"]["label"]))
        for record in graph_DAO.connections_to(id, "inflooenz_by"):
            followers.add((record["b"]["URL"], record["b"]["label"]))

    if patterns == "true":
        for record in  graph_DAO.connections_from(id, "inf_patterns_by"):
            influencers.add((record["b"]["URL"], record["b"]["label"]))
        for record in graph_DAO.connections_to(id, "inf_patterns_by"):
            followers.add((record["b"]["URL"], record["b"]["label"]))

    if classificator == "true":
        for record in  graph_DAO.connections_from(id, "inf_ML_by"):
            influencers.add((record["b"]["URL"], record["b"]["label"]))
        for record in graph_DAO.connections_to(id, "inf_ML_by"):
            followers.add((record["b"]["URL"], record["b"]["label"]))

    return influencers, followers


def lineage_artist(request):
    label = request.GET.get('q','NADA')
    inflooenz = request.GET.get('inflooenz','false')
    patterns = request.GET.get('patterns','false')
    classificator = request.GET.get('classificator', 'false')

    if inflooenz=="false" and patterns =="false" and classificator=="false":
        inflooenz = "true"

    influencers, followers = get_nodes("https://en.wikipedia.org/wiki/" + label, inflooenz, patterns, classificator)
    context = {
        'followers': followers,
        'influencers': influencers,
        'number_followers': len(followers),
        'number_influencers': len(influencers),
        'artist': label,
    }
    return render( request, 'artist_lineage.html', context)