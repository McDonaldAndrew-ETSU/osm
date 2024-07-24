# import logging
# import osmnx as ox
# from geopy.distance import geodesic
# from shapely.geometry import LineString, Point
# from sensors import HeadingController, update_position
# import matplotlib.pyplot as plt

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)


# fig, ax = plt.subplots()
# G = ox.io.load_graphml(filepath="./ccl.graphml")
# ox.plot.plot_graph(
#     G=G,
#     ax=ax,
#     node_color="orange",
#     node_size=50,  # was 0
#     node_alpha=None,
#     node_zorder=0,
#     edge_color="blue",
#     show=False,
#     close=False,
# )


# # Initial cursor position
# position = (36.3714, -82.2582)  # (lat, long)
# prev_edge_point = None

# (cursor,) = ax.plot([position[0]], [position[1]], marker="o", color="red", markersize=5)
# (nn_line,) = ax.plot([], [], color="orange", linewidth=3, linestyle="dashed")
# (ne_line,) = ax.plot([], [], color="darkcyan", linewidth=1)


# # Function to update cursor position on the plot
# def update_cursor(position):
#     cursor.set_data([position[1]], [position[0]])
#     ax.draw_artist(cursor)
#     fig.canvas.blit(ax.bbox)
#     print(f"Cursor position: {position}")


# def update_nearest_node(position):
#     nearest_node, node_dist = ox.distance.nearest_nodes(
#         G=G, X=position[1], Y=position[0], return_dist=True
#     )
#     # Get nearest node coordinates
#     nn_x = G.nodes[nearest_node]["x"]
#     nn_y = G.nodes[nearest_node]["y"]
#     # Create a LineString from position to nearest node
#     line = LineString([(position[1], position[0]), (nn_x, nn_y)])
#     x, y = line.xy
#     nn_line.set_data(x, y)
#     ax.draw_artist(nn_line)
#     fig.canvas.blit(ax.bbox)
#     print(f"Node Distance: {round(node_dist, 6)} meters")


# def update_nearest_edge(position):
#     # Find nearest edge and its geometry
#     nearest_edge, edge_dist = ox.distance.nearest_edges(
#         G=G, X=position[1], Y=position[0], return_dist=True
#     )
#     # Get nearest node coordinates
#     global prev_edge_point
#     if "geometry" in G.edges[nearest_edge]:
#         # Get the geometry LineString
#         edge_geo = G.edges[nearest_edge]["geometry"]
#         # Find the closest point on the edge to the cursor
#         point = Point(position[1], position[0])
#         edge_point = edge_geo.interpolate(edge_geo.project(point))
#         prev_edge_point = edge_point
#         # Plot line from cursor to nearest point on edge
#         line = LineString([(position[1], position[0]), (edge_point.x, edge_point.y)])
#         x, y = line.xy
#         ne_line.set_data(x, y)
#         ax.draw_artist(ne_line)
#         # Convert from degrees to meters
#         edge_dist = geodesic(
#             (position[0], position[1]), (edge_point.y, edge_point.x)
#         ).meters
#     else:
#         line = LineString(
#             [(position[1], position[0]), (prev_edge_point.x, prev_edge_point.y)]
#         )
#         x, y = line.xy
#         ne_line.set_data(x, y)
#         ax.draw_artist(ne_line)
#         # Convert from degrees to meters
#         edge_dist = geodesic(
#             (position[0], position[1]), (prev_edge_point.y, prev_edge_point.x)
#         ).meters

#     fig.canvas.blit(ax.bbox)
#     print(f"Edge Distance: {round(edge_dist, 6)} meters")


# # Connect the key press event
# heading_controller = HeadingController()
# fig.canvas.mpl_connect("key_press_event", heading_controller.on_key)


# # Set up the plot to update efficiently
# fig.canvas.draw()
# background = fig.canvas.copy_from_bbox(ax.bbox)


# while True:
#     fig.canvas.restore_region(background)
#     position = update_position(position, heading_controller.heading)
#     update_cursor(position)
#     update_nearest_edge(position)
#     update_nearest_node(position)
#     plt.pause(1)


from ui import MapNavigator
import matplotlib.pyplot as plt
from sensors import HeadingController, update_position

initial_position = (36.3714, -82.2582)  # (lat, long)
map_navigator = MapNavigator(
    graphml_path="./ccl.graphml", initial_position=initial_position
)

heading_controller = HeadingController()
map_navigator.fig.canvas.mpl_connect("key_press_event", heading_controller.on_key)

while True:
    map_navigator.fig.canvas.restore_region(map_navigator.background)
    map_navigator.position = update_position(
        map_navigator.position, heading_controller.heading
    )
    map_navigator.update_cursor(map_navigator.position)
    map_navigator.update_nearest_edge(map_navigator.position)
    map_navigator.update_nearest_node(map_navigator.position)
    plt.pause(1)
