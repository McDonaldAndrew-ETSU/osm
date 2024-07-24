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
