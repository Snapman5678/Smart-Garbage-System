import pygame
import random
import time
import itertools
import serial

# Define the map size in kilometers
MapSizeKm = 50.0

# Define the window size
WindowWidth = 800
WindowHeight = 600

# Define the radius of the node (representing waste location)
NodeRadius = 20

# Define the delay between generating garbage nodes (in milliseconds)
NodeGenerationDelay = 3000  # 3 seconds

# Serial communication settings
serial_port = 'COM3'  # Change this to match your Arduino's serial port
baud_rate = 9600

# Initialize Pygame
pygame.init()

logo_image = pygame.image.load('bbmp (1).png')

# Set the window icon
pygame.display.set_icon(logo_image)

# Create the Pygame window
window = pygame.display.set_mode((WindowWidth, WindowHeight))
pygame.display.set_caption("Waste Route Map")

# Load and resize bin images for wet waste
wet_bin_image = pygame.image.load('wet_bin.png')
wet_bin_image = pygame.transform.scale(wet_bin_image, (30, 30))  # Adjust size as needed

# Load and resize bin images for dry waste
dry_bin_image = pygame.image.load('dry_bin.png')
dry_bin_image = pygame.transform.scale(dry_bin_image, (25, 25))  # Adjust size as needed

# Load and resize background image
background_image = pygame.image.load('blore_bg.png')
background_image = pygame.transform.scale(background_image, (WindowWidth, WindowHeight))

# Load and resize BBMP image
bbmp_image = pygame.image.load('bbmp (1).png')
bbmp_image = pygame.transform.scale(bbmp_image, (70, 50))  # Adjust size as needed

# Button properties
button_color = (0, 128, 0)
button_hover_color = (0, 255, 0)
button_text_color = (255, 255, 255)
button_font = pygame.font.Font(None, 36)
button_text = button_font.render("Show Route", True, button_text_color)
button_text_rect = button_text.get_rect()
button_rect = pygame.Rect(WindowWidth - 200, WindowHeight - 50, 200, 50)

# List to store positions and images of all waste bins
wet_waste_bins = []
dry_waste_bins = []

# Initialize serial communication
try:
    ser = serial.Serial(serial_port, baud_rate)
    print("Serial connection established")
except serial.SerialException as e:
    print("Error opening serial port:", e)

# Function to generate random node
def generate_random_node():
    x = random.uniform(0, MapSizeKm - 5)
    y = random.uniform(0, MapSizeKm - 5)
    return x, y

# Function to calculate Euclidean distance between two points
def euclidean_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

# Function to calculate distance matrix
def calculate_distance_matrix(nodes):
    num_nodes = len(nodes)
    distances = [[0] * num_nodes for _ in range(num_nodes)]
    for i in range(num_nodes):
        for j in range(num_nodes):
            distances[i][j] = euclidean_distance(nodes[i], nodes[j])
    return distances

# Function to solve TSP using dynamic programming
def tsp_dynamic_programming(nodes):
    num_nodes = len(nodes)
    distances = calculate_distance_matrix(nodes)
    memo = {}

    def tsp_helper(curr, remaining):
        if (curr, remaining) in memo:
            return memo[(curr, remaining)]
        if not remaining:
            return distances[curr][0]
        min_dist = float('inf')
        for i in range(num_nodes):
            if remaining & (1 << i):
                min_dist = min(min_dist, distances[curr][i] + tsp_helper(i, remaining & ~(1 << i)))
        memo[(curr, remaining)] = min_dist
        return min_dist

    return tsp_helper(0, (1 << num_nodes) - 1)

# Function to generate TSP route
def generate_tsp_route(nodes):
    num_nodes = len(nodes)
    distances = calculate_distance_matrix(nodes)
    best_path = []
    remaining_nodes = set(range(1, num_nodes))
    curr_node = 0
    for _ in range(num_nodes - 1):
        next_node = min(remaining_nodes, key=lambda x: distances[curr_node][x])
        best_path.append(next_node)
        remaining_nodes.remove(next_node)
        curr_node = next_node
    return [0] + best_path + [0]

# Function to draw TSP route
def draw_tsp_route(route, nodes, colour):
    route_nodes = [nodes[i] for i in route]
    for i in range(len(route_nodes) - 1):
        start_pos = route_nodes[i]
        end_pos = route_nodes[i + 1]
        pygame.draw.line(window, colour, ((start_pos[0] / MapSizeKm) * WindowWidth, (start_pos[1] / MapSizeKm) * WindowHeight), ((end_pos[0] / MapSizeKm) * WindowWidth, (end_pos[1] / MapSizeKm) * WindowHeight), 2)

# Main loop
running = True
show_route = False
last_generation_time = pygame.time.get_ticks()  # Track the time of the last node generation
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                show_route = not show_route

    # Clear the window
    window.blit(background_image, (0, 0))

    # Draw BBMP logo
    window.blit(bbmp_image, (0, 0))

    # Check if it's time to generate a new node
    if not show_route and pygame.time.get_ticks() - last_generation_time >= NodeGenerationDelay:
        # Generate 5 random nodes initially
        if len(wet_waste_bins) < 5:
            waste_type = random.choice(["Wet Waste", "Dry Waste"])
            if waste_type == "Wet Waste":
                wet_waste_position = generate_random_node()
                wet_waste_bins.append(wet_waste_position)
            elif waste_type == "Dry Waste":
                dry_waste_position = generate_random_node()
                dry_waste_bins.append(dry_waste_position)
            last_generation_time = pygame.time.get_ticks()  # Update the time of the last node generation

        # Wait for input from Arduino
        if ser and ser.in_waiting > 0:
            waste_type = ser.readline().decode().strip()
            if waste_type == "Wet Waste":
                wet_waste_position = generate_random_node()
                wet_waste_bins.append(wet_waste_position)
            elif waste_type == "Dry Waste":
                dry_waste_position = generate_random_node()
                dry_waste_bins.append(dry_waste_position)
            last_generation_time = pygame.time.get_ticks()  # Update the time of the last node generation

    # Draw waste bins
    for wet_waste_position in wet_waste_bins:
        window.blit(wet_bin_image, (int((wet_waste_position[0] / MapSizeKm) * WindowWidth) - 20, int((wet_waste_position[1] / MapSizeKm) * WindowHeight) - 20))
    for dry_waste_position in dry_waste_bins:
        window.blit(dry_bin_image, (int((dry_waste_position[0] / MapSizeKm) * WindowWidth) - 20, int((dry_waste_position[1] / MapSizeKm) * WindowHeight) - 20))

    # Draw the button
    pygame.draw.rect(window, button_color, button_rect)
    window.blit(button_text, (button_rect.centerx - button_text_rect.width // 2, button_rect.centery - button_text_rect.height // 2))

    # Calculate and draw TSP routes
    if show_route:
        wet_route = generate_tsp_route([(0, 0)] + wet_waste_bins)
        draw_tsp_route(wet_route, [(0, 0)] + wet_waste_bins, [0, 255, 0])

        dry_route = generate_tsp_route([(0, 0)] + dry_waste_bins)
        draw_tsp_route(dry_route, [(0, 0)] + dry_waste_bins, [0, 0, 255])

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()

