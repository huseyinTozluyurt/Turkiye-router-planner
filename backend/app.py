import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import heapq

app = Flask(__name__)
CORS(app)

# Load and prepare distance matrix
df = pd.read_excel("ilmesafe.xlsx", sheet_name=0)
city_names = df.iloc[0, 2:].tolist()
df_clean = df.iloc[1:, 2:]
df_clean.columns = [str(col).strip().upper() for col in city_names]
df_clean.index = [str(name).strip().upper() for name in df.iloc[1:, 1].tolist()]
df_clean = df_clean.apply(pd.to_numeric, errors='coerce')

# Build graph
graph = {}
for city in df_clean.index:
    distances = df_clean.loc[city]
    neighbors = {
        str(neighbor).strip().upper(): dist
        for neighbor, dist in distances.items()
        if not np.isnan(dist)
    }
    graph[city] = neighbors

# Load coordinates CSV and normalize keys
coord_df = pd.read_csv("turkey_city_coordinates.csv")
coordinates = {
    row["City"].strip().upper(): (row["Latitude"], row["Longitude"])
    for _, row in coord_df.iterrows()
}

# Dijkstra logic
def dijkstra(graph, start, end, must_visit=None):
    if must_visit is None:
        must_visit = []

    def shortest_path(u, v):
        if u not in graph or v not in graph:
            return float('inf'), []
        visited = set()
        min_heap = [(0, u, [])]
        while min_heap:
            cost, current, path = heapq.heappop(min_heap)
            if current in visited:
                continue
            path = path + [current]
            if current == v:
                return cost, path
            visited.add(current)
            for neighbor, weight in graph[current].items():
                if neighbor not in visited:
                    heapq.heappush(min_heap, (cost + weight, neighbor, path))
        return float('inf'), []

    route = [start] + must_visit + [end]
    total_distance = 0
    full_path = []
    for i in range(len(route) - 1):
        dist, path = shortest_path(route[i], route[i + 1])
        if not path:
            return float('inf'), []
        total_distance += dist
        if full_path:
            full_path += path[1:]  # avoid repeating city
        else:
            full_path += path
    return total_distance, full_path

@app.route('/shortest-path', methods=['POST'])
def calculate_path():
    data = request.json
    start = data['start'].strip().upper()
    end = data['end'].strip().upper()
    must_visit = [city.strip().upper() for city in data.get('mustVisit', [])]

    distance, path = dijkstra(graph, start, end, must_visit)
    if path:
        return jsonify({'distance': distance, 'path': path})
    else:
        return jsonify({'error': 'No valid path found'}), 400

@app.route('/cities', methods=['GET'])
def get_cities():
    return jsonify(sorted(list(graph.keys())))

@app.route('/city-coordinates', methods=['GET'])
def get_coordinates():
    return jsonify(coordinates)


