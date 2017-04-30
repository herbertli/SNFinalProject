import json
import sys


def read_vote_data():
    """
    Reads and parses all files under the vote_data directory
    :return: Adjacency Matrix
    :rtype: Dictionary
            key: senator name (a)
            value: {} =>    key: senator name (b)
                            value: number times Senator a voted the same way as Senator b
    """
    senators_dict = {}

    democrats = []
    republicans = []
    third_party = []

    for i in range(1, 112):
        with open("vote_data/" + str(i) + ".json", "r") as f:
            data = json.load(f)

            yes_votes = []
            no_votes = []

            for s in data['votes']['Yea']:
                name = s['last_name']
                yes_votes.append(name)
                if s['party'] == "D" and name not in democrats:
                    democrats.append(name)
                elif s['party'] == "R" and name not in republicans:
                    republicans.append(name)
                elif s['party'] == "I" and name not in third_party:
                    third_party.append(name)

            for s in data['votes']['Nay']:
                name = s['last_name']
                no_votes.append(name)
                if s['party'] == "D" and name not in democrats:
                    democrats.append(name)
                elif s['party'] == "R" and name not in republicans:
                    republicans.append(name)
                elif s['party'] == "I" and name not in third_party:
                    third_party.append(name)

            for name in yes_votes:
                if name in senators_dict:
                    for other_name in yes_votes:
                        if other_name in senators_dict[name]:
                            senators_dict[name][other_name] += 1
                        else:
                            senators_dict[name][other_name] = 1
                else:
                    senators_dict[name] = {}
                    for other_name in yes_votes:
                        if other_name in senators_dict[name]:
                            senators_dict[name][other_name] += 1
                        else:
                            senators_dict[name][other_name] = 1

            for name in no_votes:
                if name in senators_dict:
                    for other_name in no_votes:
                        if other_name in senators_dict[name]:
                            senators_dict[name][other_name] += 1
                        else:
                            senators_dict[name][other_name] = 1
                else:
                    senators_dict[name] = {}
                    for other_name in no_votes:
                        if other_name in senators_dict[name]:
                            senators_dict[name][other_name] += 1
                        else:
                            senators_dict[name][other_name] = 1

    with open("senators.json", "w") as f:
        senators = {}
        senators["democrats"] = democrats
        senators["republicans"] = republicans
        senators["other"] = third_party
        f.write(json.JSONEncoder().encode(senators))

    with open("vdata.json", "w") as f:
        f.write(json.JSONEncoder().encode(senators_dict))

    return senators_dict


def read_money_data():
    """
    Reads and parses all files under the money_data directory
    :return: Industries and their respective contributions to a particular senator
    :rtype: Dictionary
            key: Industry name e.g. Lawyers, Retired, etc.
            value: {} =>    key: senator name
                            value: amount senator received from industry
    """
    industry_dict = {}

    with open("senators.json") as f:
        senator_names_dict = json.load(f)

    senator_names = []
    for key in senator_names_dict:
        for name in senator_names_dict[key]:
            senator_names.append(name)

    for name in senator_names:
        cleaned_up = name.split(" ")[-1]
        try:
            with open("money_data/" + cleaned_up + ".json", "r") as f:
                data = json.load(f)
                records = data['records']
                total = 0
                counter = 0
                for r in records:
                    counter += 1
                    total_money = r["totals"]
                    total += int(total_money)
                average = total / counter
                for r in records:
                    industry_name = r["indus"]
                    total_money = r["totals"]
                    if int(total_money) >= average:
                        if industry_name not in industry_dict:
                            industry_dict[industry_name] = {}
                        industry_dict[industry_name][name] = int(total_money)

                print("Senator", name, "received", "$" + str(total),
                      "in donations, with an average donation of", "$" + str(average))
        except IOError:
            print("Error occurred for Senator", name)

    with open("mdata.json", "w") as f:
        f.write(json.JSONEncoder().encode(industry_dict))

    return industry_dict


def convert_votes_to_graph():
    """
    Reads voting data and returns a graph representation of the data (nodes and edges/links)
    :return: Graph
    :rtype: Dictionary
            keys: "nodes" and "links" in the graph
            node: keys "name", "group"
            links: keys "source", "target", "value" (value is the percentage source votes the same as target)
    """

    with open("vdata.json") as f:
        senators_data = json.load(f)

    with open("senators.json") as f:
        senators = json.load(f)

    votes_json = {}
    senators_map = {}
    votes_json["nodes"] = []
    votes_json["links"] = []

    senators_list = list(senators_data.keys())
    for i in range(len(senators_list)):
        senators_map[senators_list[i]] = i

    for name in senators_list:
        node_dict = {}
        node_dict["name"] = name
        if name in senators["democrats"]:
            node_dict["group"] = 1
        elif name in senators["republicans"]:
            node_dict["group"] = 2
        else:
            node_dict["group"] = 3

        votes_json["nodes"].append(node_dict)

        for other_senator in senators_data[name].keys():
            link_dict = {}
            link_dict["source"] = senators_map[name]
            link_dict["target"] = senators_map[other_senator]
            link_dict["value"] = float(senators_data[name][other_senator]) / float(senators_data[name][name])
            votes_json["links"].append(link_dict)

    with open("vgraph.json", "w") as f:
        f.write(json.JSONEncoder().encode(votes_json))
    return votes_json


def convert_industries_to_graph():
    """
    Reads industry data and returns a graph representation of the data (nodes and edges/links)
    :return: Graph
    :rtype: Dictionary
            keys: "nodes" and "links" in the graph
            node: keys "name", "group"
            links: keys "source", "target", "value" (value is the percentage source votes the same as target)
    """
    with open("mdata.json") as f:
        data = json.load(f)

    with open("senators.json") as f:
        senators = json.load(f)

    money_json = {}
    adj_matrix = {}
    senators_map = {}
    money_json["nodes"] = []
    money_json["links"] = []

    democrats = senators["democrats"]
    republicans = senators["republicans"]
    other = senators["other"]
    all_senators = []
    for i in democrats:
        all_senators.append(i)
    for i in republicans:
        all_senators.append(i)
    for i in other:
        all_senators.append(i)
    for i in range(len(all_senators)):
        node_dict = {}
        node_dict["name"] = all_senators[i]
        if all_senators[i] in democrats:
            node_dict["group"] = 1
        elif all_senators[i] in republicans:
            node_dict["group"] = 2
        else:
            node_dict["group"] = 3
        senators_map[all_senators[i]] = i
        money_json["nodes"].append(node_dict)

    industries = data.keys()
    for industry in industries:
        senators = data[industry].keys()
        for senator in senators:
            if senator not in adj_matrix:
                adj_matrix[senator] = {}
            for other_senator in senators:
                if other_senator not in adj_matrix[senator]:
                    adj_matrix[senator][other_senator] = 1
                else:
                    adj_matrix[senator][other_senator] += 1

    for senator in adj_matrix:
        for other_senator in adj_matrix[senator]:
            links_dict = {}
            links_dict["source"] = senators_map[senator]
            links_dict["target"] = senators_map[other_senator]
            links_dict["value"] = adj_matrix[senator][other_senator] / adj_matrix[senator][senator]
            money_json["links"].append(links_dict)

    with open("mgraph.json", "w") as f:
        f.write(json.JSONEncoder().encode(money_json))
    return money_json


if __name__ == "__main__":
    if len(sys.argv) == 1:
        while True:
            print("Read (v)ote data")
            print("Read (i)ndustry data")
            print("Get vote (a)djacency matrix")
            print("Get industry a(d)jacency matrix")
            print("(e)xit")
            print()
            choice = input("Enter a command: ")
            if choice == "e":
                break
            elif choice == "v":
                read_vote_data()
            elif choice == "i":
                read_money_data()
            elif choice == "a":
                convert_votes_to_graph()
            elif choice == "d":
                convert_industries_to_graph()
            elif choice == "e":
                break
            else:
                print("Invalid command")
            print()
    else:
        if sys.argv[1] == "v":
            read_vote_data()
        elif sys.argv[1] == "i":
            read_money_data()
        elif sys.argv[1] == "a":
            convert_votes_to_graph()
        elif sys.argv[1] == "d":
            convert_industries_to_graph()
        else:
            print("Invalid command")
