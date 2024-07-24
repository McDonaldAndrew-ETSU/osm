import osmnx as ox
import matplotlib.pyplot as plt
import math

# Define the bounding box (Lng/Lat) in WGS84
bbox = (36.3823, 36.3657, -82.2656, -82.2453)

# Download the road network within the bounding box
G = ox.graph_from_bbox(bbox=bbox, network_type="all")

ox.io.save_graphml(G, filepath="./ccl.graphml", gephi=False, encoding="utf-8")
