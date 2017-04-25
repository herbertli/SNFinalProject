import json


def read_vote_data():
    senators_dict = {}

    # there are 111 files to read
    for i in range(1, 112):
        with open("vote_data/" + str(i) + ".json", "r") as f:
            data = json.load(f)

            yes_votes = []
            no_votes = []
            for s in data['votes']['Yea']:
                name = s['first_name'] + " " + s['last_name']
                yes_votes.append(name)

            for s in data['votes']['Nay']:
                name = s['first_name'] + " " + s['last_name']
                no_votes.append(name)

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

    # for name in senators_dict:
    #     print(name, senators_dict[name][name])

    # print(len(senators_dict.keys()))
    with open("vdata.json", "w") as f:
        f.write(json.JSONEncoder().encode(senators_dict))
    return senators_dict


def read_money_data(senator_names):
    industry_dict = {}

    for name in senator_names:
        last_name = name.split(" ")[-1]
        try:
            with open("money_data/" + last_name + ".json", "r") as f:
                data = json.load(f)
                records = data['records']
                for r in records:
                    industry_name = r["indus"]
                    total_money = r["totals"]
                    if industry_name not in industry_dict:
                        industry_dict[industry_name] = {}
                    industry_dict[industry_name][name] = total_money
        except:
            print(name, "error occured!!!")


    with open("mdata.json", "w") as f:
        f.write(json.JSONEncoder().encode(industry_dict))

    return industry_dict

senators = read_vote_data()
senator_names = senators.keys()
industries = read_money_data(senator_names)
print(sorted(industries.keys()))
# for k in industries:
#     print(k)
#     print("================")
#     print(industries[k])
