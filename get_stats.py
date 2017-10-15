import read_data
import networkx


def filter_edges(G, threshold):
    new_G = networkx.Graph()
    new_G.add_nodes_from(G.nodes)
    new_G.add_edges_from(filter((lambda x: G.edges[x]['value'] * 100 >= threshold), G.edges))
    return new_G


def get_stats(G, threshold):
    new_G = filter_edges(G, threshold)
    diameter = max([networkx.diameter(c) for c in networkx.connected_component_subgraphs(new_G)])
    average = networkx.average_shortest_path_length(G)
    components = networkx.number_connected_components(G)
    print("Average distance is", average)
    print("Diameter of graph is", diameter)
    print("Number of components is", components)


if __name__ == "__main__":
    votes_json = read_data.convert_votes_to_graph()
    money_json = read_data.convert_industries_to_graph()
    votes_graph = networkx.node_link_graph(votes_json)
    money_graph = networkx.node_link_graph(money_json)

    for threshold in range(50, 101, 5):
        print("Threshold:", threshold)
        print("===================")
        print("Voting data:")
        print("===================")
        get_stats(votes_graph, threshold)
        print("Money data:")
        print("===================")
        get_stats(money_graph, threshold)