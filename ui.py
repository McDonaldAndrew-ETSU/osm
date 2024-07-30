import logging
import osmnx as ox
from geopy.distance import geodesic
from shapely.geometry import LineString, Point
import matplotlib.pyplot as plt


class MapNavigator:
    def __init__(self, graphml_path, initial_position):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        self.map_matching = False
        self.G = ox.io.load_graphml(filepath=graphml_path)
        self.position = initial_position
        self.prev_edge_point = None

        # Initialize plot
        self.fig, self.ax = plt.subplots()
        ox.plot.plot_graph(
            G=self.G,
            ax=self.ax,
            node_color="orange",
            node_size=50,  # was 0
            node_alpha=None,
            node_zorder=0,
            edge_color="blue",
            show=False,
            close=False,
        )
        (self.cursor,) = self.ax.plot(
            [self.position[0]],
            [self.position[1]],
            marker="o",
            color="red",
            markersize=5,
        )
        (self.nn_line,) = self.ax.plot(
            [], [], color="orange", linewidth=3, linestyle="dashed"
        )
        (self.ne_line,) = self.ax.plot([], [], color="darkcyan", linewidth=1)

        # Set up the plot to update efficiently
        self.fig.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)

    def update_cursor(self, position):
        edge_dist = self._update_nearest_edge(position)
        node_dist, node_position = self._update_nearest_node(position)
        if self.map_matching:
            # if edge_dist > 10 and node_dist < 10 and self.prev_edge_point is not None:
            #     position = (node_position.x, node_position.y)
            # el
            if edge_dist > 10 and self.prev_edge_point is not None:
                position = (self.prev_edge_point.x, self.prev_edge_point.y)

        self.cursor.set_data([position[1]], [position[0]])
        self.ax.draw_artist(self.cursor)
        self.fig.canvas.blit(self.ax.bbox)
        self.logger.info(f"Cursor position: {position}")

    def _update_nearest_node(self, position):
        nearest_node, node_dist = ox.distance.nearest_nodes(
            G=self.G, X=position[1], Y=position[0], return_dist=True
        )
        # Get nearest node coordinates
        nn_x = self.G.nodes[nearest_node]["x"]
        nn_y = self.G.nodes[nearest_node]["y"]
        # Create a LineString from position to nearest node
        line = LineString([(position[1], position[0]), (nn_x, nn_y)])
        x, y = line.xy
        self.nn_line.set_data(x, y)
        self.ax.draw_artist(self.nn_line)
        self.fig.canvas.blit(self.ax.bbox)
        self.logger.info(f"Node Distance: {round(node_dist, 6)} meters")
        return node_dist, (nn_x, nn_y)

    def _update_nearest_edge(self, position):
        # Find nearest edge and its geometry
        nearest_edge, edge_dist = ox.distance.nearest_edges(
            G=self.G, X=position[1], Y=position[0], return_dist=True
        )
        # Get nearest node coordinates
        if "geometry" in self.G.edges[nearest_edge]:
            # Get the geometry LineString
            edge_geo = self.G.edges[nearest_edge]["geometry"]
            # Find the closest point on the edge to the cursor
            point = Point(position[1], position[0])
            edge_point = edge_geo.interpolate(edge_geo.project(point))
            self.prev_edge_point = edge_point
            # Plot line from cursor to nearest point on edge
            line = LineString(
                [(position[1], position[0]), (edge_point.x, edge_point.y)]
            )
            x, y = line.xy
            self.ne_line.set_data(x, y)
            self.ax.draw_artist(self.ne_line)
            # Convert from degrees to meters
            edge_dist = geodesic(
                (position[1], position[0]), (edge_point.x, edge_point.y)
            ).meters
        elif self.prev_edge_point is not None:
            line = LineString(
                [
                    (position[1], position[0]),
                    (self.prev_edge_point.x, self.prev_edge_point.y),
                ]
            )
            x, y = line.xy
            self.ne_line.set_data(x, y)
            self.ax.draw_artist(self.ne_line)
            # Convert from degrees to meters
            edge_dist = geodesic(
                (position[1], position[0]),
                (self.prev_edge_point.x, self.prev_edge_point.y),
            ).meters
        else:
            self.logger.info("No previous edge point available. Skipping line drawing.")
            edge_dist = float("inf")

        self.fig.canvas.blit(self.ax.bbox)
        self.logger.info(f"Edge Distance: {round(edge_dist, 6)} meters")
        return edge_dist
