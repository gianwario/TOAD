import csv
from community import community
def get_input_communities(path):
    communities = []
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            communities.append(community.Community(row[0], row[1]))
    return communities