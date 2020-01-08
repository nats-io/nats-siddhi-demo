import csv
import json


def get_stops(line, bound):
    # url = f"https://api.tfl.gov.uk/line/{line}/route/sequence/{bound}"
    # r = requests.get(url=url)
    # stop_points = r.json()
    with open('./sample-data/sequence-inbound.json', 'r') as f:
        data = json.load(f)
    stop_points = data["stopPointSequences"][0]["stopPoint"]

    stop_info = list()
    for stop_point in stop_points:
        stop_info.append([line, bound, stop_point["id"], stop_point["name"], stop_point["lat"], stop_point["lon"]])
    return stop_info


if __name__ == "__main__":
    root_line = input("Bus line number to generate bus stop details?\n")
    # stops =  + get_stops(line, 'outbound')
    with open('stops.csv', 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(get_stops(root_line, 'inbound') + get_stops(root_line, 'outbound'))
