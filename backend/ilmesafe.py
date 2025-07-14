import pandas as pd
import numpy as np
import heapq

# Load and clean the Excel file
df = pd.read_excel("ilmesafe.xlsx", sheet_name=0)

# Extract city names and distance matrix
city_names = df.iloc[0, 2:].tolist()
df_clean = df.iloc[1:, 2:]
df_clean.columns = [str(col).strip().upper() for col in city_names]
df_clean.index = [str(name).strip().upper() for name in df.iloc[1:, 1].tolist()]
df_clean = df_clean.apply(pd.to_numeric, errors='coerce')

# Build the graph
graph = {}
for city in df_clean.index:
    distances = df_clean.loc[city]
    neighbors = {
        str(neighbor).strip().upper(): dist
        for neighbor, dist in distances.items()
        if not np.isnan(dist)
    }
    graph[city] = neighbors

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
            print(f"⚠️ No path found from {route[i]} to {route[i + 1]}")
            return float('inf'), []
        total_distance += dist
        if full_path:
            full_path += path[1:]  # avoid duplicate
        else:
            full_path += path
    return total_distance, full_path

# Real user input version
def user_input_shortest_path(graph):
    print("📍 Welcome to Türkiye City Shortest Route Finder!\n")
    print("📌 Available cities:")
    city_list = list(graph.keys())
    for i, city in enumerate(city_list):
        print(f"{i + 1}. {city}")

    def get_city_input(prompt):
        while True:
            city = input(prompt).strip().upper()
            if city in graph:
                return city
            else:
                print("❌ Invalid city name. Please try again.")

    start = get_city_input("\n🔹 Enter the starting city: ")
    end = get_city_input("🔹 Enter the destination city: ")

    must_visit = []
    while True:
        try:
            count = int(input("🔸 How many cities do you want to visit during your vacation? "))
            break
        except ValueError:
            print("⚠️ Please enter a valid number.")

    print("\n✏️ Now enter the cities to visit:")
    while len(must_visit) < count:
        city = input(f"City {len(must_visit)+1}: ").strip().upper()
        if city not in graph:
            print("❌ Invalid city name.")
        elif city == start or city == end:
            print("⚠️ This city is already selected as start or destination.")
        elif city in must_visit:
            print("⚠️ City already added.")
        else:
            must_visit.append(city)

    total_distance, full_path = dijkstra(graph, start, end, must_visit)

    print("\n✅ Shortest Route:")
    if full_path:
        print(" → ".join(full_path))
        print(f"📏 Total Distance: {total_distance} km")
    else:
        print("❌ No valid path found.")

# 🚀 Run the interactive program
user_input_shortest_path(graph)
