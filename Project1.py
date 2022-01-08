from networkx.algorithms.centrality import closeness
from networkx.algorithms.centrality.betweenness import betweenness_centrality
import tweepy
import json
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()


auth = tweepy.OAuthHandler("SBTYXKxsFDD5NZqcSYlb3NjlJ", "rgDUOaBQxmcAlUQjltHKfnaXRLc5KJlRdkFl4GAOuy11a6l6Ha")
auth.set_access_token("1439801089625186309-jFCFrotbcdmeUPTYE5DXTBdRhyC6ez", "ZVtzK8brRPVUivz75HIBr2L0m1F9yB5YpLS9Fu0QyhgpI")

api = tweepy.API(auth)
api.wait_on_rate_limit = True
api.wait_on_rate_limit_notify = True

elon = api.get_user(screen_name = 'elonmusk').id
elon_following = api.get_friend_ids(user_id = elon)
userjsonlist = []

def obj_dict(obj):
        return obj.__dict__

#for friend in elon_following:
    #friendslist = api.get_friend_ids(user_id = friend)
    #name = friend
    #filename = "%s.json" % name
    #with open(filename, 'w') as outfile:
        #outfile.write(json.dumps(friendslist, default=obj_dict, indent = 4))

def findfriend(userid):
    followlist = []
    f = open("%s.json" % userid)
    tempList = json.load(f)
    setList = set(tempList)
    mutual = setList.intersection(elon_following)
    mutualList = list(mutual)
    if(elon in setList):
        mutualList.append(elon)
    return mutualList

class Person:
    def __init__(self, name, screen_n, id, follows):
        self.name = name
        self.screen_n = screen_n
        self.id = id
        self.follows = follows

def createnode(user):
    flist = findfriend(user)
    json.dumps(flist, default=obj_dict)
    node = Person(api.get_user(user_id = user).name, api.get_user(user_id = user).screen_name, user, flist)
    G.add_node(node.screen_n)
    userjsonlist.append(node)

for users in elon_following:
    createnode(users)
   

elonNode = Person(api.get_user(user_id = elon).name, api.get_user(user_id = elon).screen_name, elon, elon_following)
userjsonlist.append(elonNode)
#G.add_node(elonNode.screen_n)

with open('data.json', 'w') as outfile:
    outfile.write(json.dumps(userjsonlist, default=obj_dict, indent = 4))

for ujl in userjsonlist:
    tempfollowing = ujl.follows
    #print("FIRST")
    for p in tempfollowing:
        #print("B4 add edge")
        G.add_edge(ujl.screen_n, api.get_user(user_id = p).screen_name)
        #print("AFTER add edge")

def plot_degree_hist(G):
    degrees = [G.degree(n) for n in G.nodes()]
    plt.figure(figsize= (15,15))
    plt.title("Degree Dist.")
    plt.xlabel("Degree")
    plt.ylabel("Count")
    plt.hist(degrees, bins = 'auto')
    plt.savefig('degGraph.png')




#plt.hist(nx.centrality.betweenness_centrality(G).values())
#plt.savefig("betGraph.png")
plt.hist(nx.centrality.closeness_centrality(G).values())
plt.savefig("closenessGraph.png")
#plot_degree_hist(G)
space = nx.spring_layout(G, k = .15, iterations = 20)
plt.figure(figsize= (30,30))
nx.draw(G, pos = space, node_size = 800, with_labels = True, font_size = 8, font_weight = 'bold')
plt.savefig("graph.png")