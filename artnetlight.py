import pygame
import requests

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUM_LIGHTS = 8
LIGHT_RADIUS = 10
STAGE_WIDTH = 600  # Width of the stage cube
STAGE_HEIGHT = 100  # Height of the stage cube
STAGE_DEPTH = 100  # Depth of the stage cube
STAGE_COLOR = (100, 100, 100)
BEAM_SPEED = 3  # Speed of beam expansion
MAX_BEAM_WIDTH = 30  # Maximum width of the beam

# Function to make HTTP request and get ArtNet data
def get_artnet_data():
    try:
        response = requests.get("http://localhost:9090/get_dmx?u=1")
        data = response.json()["dmx"]
        return data
    except Exception as e:
        print("Error:", e)
        return [0] * (NUM_LIGHTS * 5)  # Return default data if request fails

# Function to draw lights and their expanding beams on the screen
def draw_lights(screen, artnet_data):
    for i in range(NUM_LIGHTS):
        light_index = i * 5
        brightness_index = light_index
        red_index = light_index + 1
        blue_index = light_index + 2
        green_index = light_index + 3
        saturation_index = light_index + 4
        
        # Get brightness from the channel before red channel
        brightness = artnet_data[brightness_index]
        r = artnet_data[red_index]
        g = artnet_data[blue_index]
        b = artnet_data[green_index]
        s = artnet_data[saturation_index]
        
        x = ((i + 1) / (NUM_LIGHTS + 1)) * (SCREEN_WIDTH - STAGE_WIDTH) + STAGE_WIDTH / 2
        y = SCREEN_HEIGHT - LIGHT_RADIUS
        z = STAGE_DEPTH // 2
        
        # Adjust color intensity based on brightness
        r = min(int(r * brightness / 255), 255)
        g = min(int(g * brightness / 255), 255)
        b = min(int(b * brightness / 255), 255)
        
        color = (r, g, b)
        pygame.draw.circle(screen, color, (int(x), int(y)), LIGHT_RADIUS)
        
        # Draw expanding beam with adjusted brightness
        for h in range(0, SCREEN_HEIGHT, BEAM_SPEED):
            distance_to_light = abs(SCREEN_HEIGHT - h)
            beam_width = min(distance_to_light / 10, MAX_BEAM_WIDTH)
            beam_brightness = min(brightness * 2, 255)  # Adjust brightness of the beam
            beam_color = (r, g, b)  # Maintain the RGB color of the beam
            pygame.draw.line(screen, beam_color, (int(x - beam_width / 2), h), (int(x + beam_width / 2), h), 2)

# Function to draw the stage cube
def draw_stage(screen):
    stage_rect = pygame.Rect((SCREEN_WIDTH - STAGE_WIDTH) // 2, SCREEN_HEIGHT - STAGE_HEIGHT, STAGE_WIDTH, STAGE_HEIGHT)
    pygame.draw.rect(screen, STAGE_COLOR, stage_rect, 3)

# Main function
def main():
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ArtNet Simulator")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get ArtNet data from HTTP request
        artnet_data = get_artnet_data()

        # Fill the background
        screen.fill((0, 0, 0))

        # Draw stage
        draw_stage(screen)

        # Draw lights and beams
        draw_lights(screen, artnet_data)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
