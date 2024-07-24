import math


# Placeholder functions for sensor data
def get_wheel_distance():
    return 0.0005


class HeadingController:
    def __init__(self):
        self.heading = 0

    def on_key(self, event):
        if event.key == "up":
            self.heading = (self.heading + 10) % 360
        elif event.key == "down":
            self.heading = (self.heading - 10) % 360

        print(f"Heading: {self.heading}°")


# Function to update position based on sensor data and map-matching
def update_position(position, heading):
    distance = get_wheel_distance()

    # Convert heading to radians
    heading_rad = math.radians(heading)

    # Calculate new position
    delta_x = distance * math.cos(heading_rad)
    delta_y = distance * math.sin(heading_rad)

    # Update position
    position = (round((position[0] + delta_x), 4), round((position[1] + delta_y), 4))

    # Snap to nearest road if within a small tolerance

    return position
