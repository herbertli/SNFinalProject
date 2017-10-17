import json
import glob
import os
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from functools import reduce


class Senator:

    def __init__(self, senator_dict=None):
        self.yea_votes = []
        self.no_votes = []
        self.industries = {}
        self.has_outliers = True
        if senator_dict:
            self.display_name = senator_dict['display_name']
            self.first_name = senator_dict['first_name']
            self.last_name = senator_dict['last_name']
            self.id = senator_dict['id']
            self.party = senator_dict['party']
            self.state = senator_dict['state']

    def vote_similarity(self, other):
        same = 0
        for vote in self.yea_votes:
            if vote in other.yea_votes:
                same += 1
        for vote in self.no_votes:
            if vote in other.no_votes:
                same += 1
        return same / (len(self.yea_votes) + len(self.no_votes) + len(other.yea_votes) + len(other.no_votes) - same)

    def money_similarity(self, other):
        if self.has_outliers:
            self.remove_outliers()
        if other.has_outliers:
            other.remove_outliers()
        same = 0
        for industry_id in self.industries.keys():
            if industry_id in other.industries.keys():
                same += 1
        return same / (len(self.industries.keys()) + len(other.industries.keys()) - same)
        # return same / len(self.industries.keys()) ** .5 / len(other.industries.keys()) ** .5

    def add_yea(self, vote_id):
        self.yea_votes.append(vote_id)

    def add_no(self, vote_id):
        self.no_votes.append(vote_id)

    def add_industry(self, industry_id, amount):
        if industry_id not in self.industries.keys():
            self.industries[industry_id] = amount
        else:
            self.industries[industry_id] += amount

    def remove_outliers(self, m=2):
        data = list(self.industries.values())
        med = np.median(data)
        d = np.abs(data - med)
        mdev = np.median(d)
        removed_keys = [k for k in self.industries.keys() if self.industries[k] / mdev > m]
        for k in removed_keys:
            del self.industries[k]
        self.has_outliers = False


def read_vote_data():
    """
    Reads and parses all files under the vote_data directory
    :return: List of Senator objects
    :rtype: List
    """
    senators_dict = {}

    for i in range(1, 112):
        with open("vote_data/" + str(i) + ".json", "r") as f:
            data = json.load(f)

            yes_votes = data['votes']['Yea']
            no_votes = data['votes']['Nay']
            vote_id = data['vote_id']

            for senator in yes_votes:
                if senator['id'] not in senators_dict:
                    senators_dict[senator['id']] = Senator(senator)
                senators_dict[senator['id']].add_yea(vote_id)

            for senator in no_votes:
                if senator['id'] not in senators_dict:
                    senators_dict[senator['id']] = Senator(senator)
                senators_dict[senator['id']].add_no(vote_id)
    return list(senators_dict.values())


def read_money_data():
    """
    Reads and parses all files under the money_data directory
    :return: List of Industry objects
    :rtype: List
    """
    senators_dict = {}

    for filename in glob.glob(os.path.join("money_data/", "*.json")):
        with open(filename) as f:
            data = json.load(f)
            for record in data['records']:
                if 'memname' not in record.keys():
                    continue
                if record['memname'] not in senators_dict:
                    senators_dict[record['memname']] = Senator()
                    senators_dict[record['memname']].display_name = record['memname']
                senators_dict[record['memname']].add_industry(record['indus'], float(record['totals']))

    return list(senators_dict.values())


def convert_votes_to_graph():
    """
    Reads voting data and returns a graph representation of the data (nodes and edges/links)
    :return: d3-compatible dictionary
    :rtype: Dictionary
    """
    senators = read_vote_data()

    party_map = {
        'R': 2,
        'D': 1,
        'I': 3
    }

    G = nx.Graph()
    for i in range(len(senators)):
        G.add_node(i, name=senators[i].display_name, group=party_map[senators[i].party])

    removed = 0
    for i in range(len(senators)):
        for j in range(i + 1, len(senators)):
            sim = senators[i].vote_similarity(senators[j])
            if sim >= .5:
                G.add_edge(i, j, value=min(sim, 1))
            else:
                removed += 1

    print("Added:", len(G.nodes), "nodes")
    print("Added:", len(G.edges), "edges, removed", removed)

    assert len(G.nodes) == len(senators)
    for x, y in G.edges:
        assert x in G.nodes
        assert y in G.nodes

    return nx.node_link_data(G)


def convert_industries_to_graph():
    """
    Reads industry data and returns a graph representation of the data (nodes and edges/links)
    :return: Graph
    :rtype: Dictionary
            keys: "nodes" and "links" in the graph
            node: keys "name", "group"
            links: keys "source", "target", "value" (value is the percentage source votes the same as target)
    """
    senators = read_money_data()

    party_map = {
        'R': 2,
        'D': 1,
        'I': 3
    }

    G = nx.Graph()
    for i in range(len(senators)):
        G.add_node(i, name=senators[i].display_name, group=party_map[senators[i].display_name[-2]])

    removed = 0
    for i in range(len(senators)):
        for j in range(i + 1, len(senators)):
            sim = senators[i].money_similarity(senators[j])
            if sim >= .5:
                G.add_edge(i, j, value=min(sim, 1))
            else:
                removed += 1

    print("Added:", len(G.nodes), "nodes")
    print("Added:", len(G.edges), "edges, removed", removed)

    assert len(G.nodes) == len(senators)
    for x, y in G.edges:
        assert x in G.nodes
        assert y in G.nodes
    return nx.node_link_data(G)


def plot_senators():
    senators = read_vote_data()
    senator_names = [senator.display_name for senator in senators]
    yea_votes = [len(senator.yea_votes) for senator in senators]
    no_votes = [len(senator.no_votes) for senator in senators]
    fig, ax = plt.subplots()
    index = np.arange(len(senator_names))
    bar_width = 0.35
    opacity = 0.4

    rects1 = ax.bar(index, yea_votes, bar_width, alpha=opacity, color='b', label='Yea')
    rects2 = ax.bar(index + bar_width, no_votes, bar_width, alpha=opacity, color='r', label='Nay')

    ax.set_xlabel('Senator')
    ax.set_ylabel('Number of Votes')
    ax.set_title('Voting Patterns of Senators')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(senator_names)
    ax.legend()
    plt.show()


def plot_industries():
    plt.rcdefaults()
    fig, ax = plt.subplots()

    senators = read_money_data()
    senator_names = [senator.display_name for senator in senators]

    y_pos = np.arange(len(senators))
    totals = [reduce((lambda x, y: x + y), list(senator.donations.values())) for senator in senators]
    ax.barh(y_pos, totals)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(senator_names)
    ax.invert_yaxis()
    ax.set_xlabel('Senator')
    ax.set_title('Total Contributions Received by Senator')
    plt.show()

if __name__ == "__main__":
    votes_json = convert_votes_to_graph()
    money_json = convert_industries_to_graph()

    with open("mgraph.json", "w") as f:
        f.write(json.JSONEncoder().encode(money_json))

    with open("vgraph.json", "w") as f:
        f.write(json.JSONEncoder().encode(votes_json))

