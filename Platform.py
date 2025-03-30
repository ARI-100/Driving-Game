import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CAR_WIDTH = 50  # Desired width for the player car
CAR_HEIGHT = 100  # Desired height for the player car
FPS = 60
OBSTACLE_TARGET_WIDTH = 70  # Desired width for other obstacle cars
OBSTACLE_TARGET_HEIGHT = 120  # Desired height for other obstacle cars
ORANGE_CAR_WIDTH = 180  # New width for the orange car
ORANGE_CAR_HEIGHT = 180  # New height for the orange car
COLLECTIBLE_RADIUS = 15  # Radius of the collectible circle
HITBOX_WIDTH = 40  # Width of the hitbox (adjust as needed)
HITBOX_HEIGHT = 95  # Height of the hitbox (adjust as needed)
HITBOX_OFFSET = -10  # Offset for the hitbox above the car

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Drift Game")

# Load images
background_image = pygame.image.load('highway.png')  # Replace with your city image path
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

car_image = pygame.image.load('car_image.png')  # Replace with your player car image path
car_image = pygame.transform.scale(car_image, (CAR_WIDTH, CAR_HEIGHT))  # Scale to fixed dimensions

# Load multiple obstacle car images
obstacle_car_images = [
    pygame.image.load('obstacle_car_image1.png'),  # Orange car (first image)
    pygame.image.load('obstacle_car_image2.png'),  # Second obstacle car
    pygame.image.load('obstacle_car_image3.png'),  # Third obstacle car
]

# Scale the orange car to be bigger with defined dimensions
obstacle_car_images[0] = pygame.transform.scale(obstacle_car_images[0], 
    (ORANGE_CAR_WIDTH, ORANGE_CAR_HEIGHT))

# Scale the other obstacle car images while maintaining aspect ratio
def scale_image(image, target_width, target_height):
    original_width, original_height = image.get_size()
    aspect_ratio = original_width / original_height
    if aspect_ratio > 1:  # Wider than tall
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:  # Taller than wide
        new_height = target_height
        new_width = int(target_height * aspect_ratio)
    return pygame.transform.scale(image, (new_width, new_height)), (new_width, new_height)

# Scale all other obstacle car images and get their new dimensions
obstacle_car_images[1] = scale_image(obstacle_car_images[1], OBSTACLE_TARGET_WIDTH, OBSTACLE_TARGET_HEIGHT)[0]
obstacle_car_images[2] = scale_image(obstacle_car_images[2], OBSTACLE_TARGET_WIDTH, OBSTACLE_TARGET_HEIGHT)[0]

# Game variables
car_x = SCREEN_WIDTH // 2 - CAR_WIDTH // 2
car_y = SCREEN_HEIGHT - CAR_HEIGHT - 20
car_speed = 0  # Start with zero speed
max_speed = 10  # Maximum speed limit
acceleration = 0.8  # Speed increase per frame
deceleration = 1  # Speed decrease when keys are not pressed
obstacles = []
collectibles = []  # List to hold collectibles
obstacle_speed = 8
obstacle_spawn_time = 30  # Frames until a new obstacle spawns
collectible_spawn_time = 150  # Frames until a new collectible spawns
obstacle_timer = 0
collectible_timer = 0
score = 0
score_increment_time = 100  # Time in milliseconds to increment score
score_timer = 0  # Timer for score increment
font = pygame.font.Font(None, 36)

# Power-up types
POWER_UPS = {
    "speed_boost": (0, 0, 255),  # Blue for speed boost
    "invincibility": (255, 0, 0),  # Red for invincibility
}

# Game loop
clock = pygame.time.Clock()
game_over = False
invincible = False  # Flag for invincibility
invincibility_duration = 10000  # Duration of invincibility in milliseconds (10 seconds)
invincibility_timer = 0  # Timer for invincibility
power_up_message = ""  # Message to display when a power-up is collected
message_timer = 0  # Timer for how long to display the message
game_start_time = pygame.time.get_ticks()  # Record the start time of the game

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Get key states
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_speed = min(car_speed + acceleration, max_speed)  # Gradually increase speed
            car_x -= car_speed  # Move left
        elif keys[pygame.K_RIGHT]:
            car_speed = min(car_speed + acceleration, max_speed)  # Gradually increase speed
            car_x += car_speed  # Move right
        else:
            # Gradually decrease speed when keys are not pressed
            car_speed = max(0, car_speed - deceleration)

        # Keep the car within the screen bounds
        car_x = max(0, min(car_x, SCREEN_WIDTH - CAR_WIDTH))

        # Obstacle spawning
        obstacle_timer += 1
        if obstacle_timer >= obstacle_spawn_time:
            obstacle_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_TARGET_WIDTH)
            obstacle_image = random.choice(obstacle_car_images)
            obstacle_rect = pygame.Rect(obstacle_x, 0, obstacle_image.get_width(), obstacle_image.get_height())
            obstacles.append((obstacle_image, obstacle_rect))
            obstacle_timer = 0

        # Collectible spawning
        collectible_timer += 1
        if collectible_timer >= collectible_spawn_time:
            collectible_x = random.randint(0, SCREEN_WIDTH - COLLECTIBLE_RADIUS * 2)  # Adjust for circle
            collectible_type = random.choice(list(POWER_UPS.keys()))  # Randomly choose a power-up type
            collectible_rect = pygame.Rect(collectible_x, 0, COLLECTIBLE_RADIUS * 2, COLLECTIBLE_RADIUS * 2)  # Circle bounding box
            collectibles.append((collectible_rect, collectible_type))  # Store the type with the collectible
            collectible_timer = 0

        # Update obstacle positions
        for _, obstacle in obstacles:
            obstacle.y += obstacle_speed

        # Update collectible positions
        for collectible, _ in collectibles:
            collectible.y += obstacle_speed  # Move collectibles down with the same speed as obstacles

        # Remove off-screen obstacles and collectibles
        obstacles = [(image, obstacle) for image, obstacle in obstacles if obstacle.y < SCREEN_HEIGHT]
        collectibles = [(collectible, type) for collectible, type in collectibles if collectible.y < SCREEN_HEIGHT]

        # Collision detection
        car_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
        player_hitbox_rect = pygame.Rect(car_x + (CAR_WIDTH - HITBOX_WIDTH) // 2, car_y - HITBOX_OFFSET, HITBOX_WIDTH, HITBOX_HEIGHT)
        
        # Check for collisions with obstacles
        for _, obstacle in obstacles:
            hitbox_rect = pygame.Rect(obstacle.x + (obstacle.width - HITBOX_WIDTH) // 2, obstacle.y - HITBOX_OFFSET, HITBOX_WIDTH, HITBOX_HEIGHT)
            if player_hitbox_rect.colliderect(hitbox_rect) and not invincible:
                game_over = True

        # Check for collisions with collectibles
        for collectible, collectible_type in collectibles:
            if car_rect.colliderect(collectible):
                if collectible_type == "speed_boost":
                    car_speed += 2  # Increase speed temporarily
                    power_up_message = "Speed Boost Activated!"  # Set power-up message
                    message_timer = pygame.time.get_ticks()  # Start message timer
                elif collectible_type == "invincibility":
                    invincible = True  # Set a flag for invincibility
                    invincibility_timer = pygame.time.get_ticks()  # Start the invincibility timer
                    power_up_message = "Invincibility Activated!"  # Set power-up message
                    message_timer = pygame.time.get_ticks()  # Start message timer
                score += 15  # Increase score for collecting an item
                collectibles.remove((collectible, collectible_type))  # Remove the collectible from the list

        # Update score based on time
        score_timer += clock.get_time()  # Increment score timer by the time since the last frame
        if score_timer >= score_increment_time:
            score += 1  # Increment score
            score_timer = 0  # Reset score timer

        # Handle invincibility duration
        if invincible:
            remaining_time = invincibility_duration - (pygame.time.get_ticks() - invincibility_timer)
            if remaining_time <= 0:
                invincible = False  # Reset invincibility after duration

        # Handle power-up message display duration
        if message_timer and pygame.time.get_ticks() - message_timer > 3000:  # Show message for 3 seconds
            power_up_message = ""  # Clear message

        # Draw everything
        screen.blit(background_image, (0, 0))
        screen.blit(car_image, (car_x, car_y))
        for obstacle_image, obstacle in obstacles:
            screen.blit(obstacle_image, (obstacle.x, obstacle.y))
        for collectible, collectible_type in collectibles:
            # Draw collectibles with their respective colors
            color = POWER_UPS[collectible_type]  # Get the color based on the type
            pygame.draw.circle(screen, color, (collectible.x + COLLECTIBLE_RADIUS, collectible.y + COLLECTIBLE_RADIUS), COLLECTIBLE_RADIUS)  # Draw circle

        # Draw score
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Draw power-up message
        if power_up_message:
            message_text = font.render(power_up_message, True, (255, 255, 0))  # Yellow text for the message
            screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))

        # Draw power-up timer
        if invincible:
            remaining_time = invincibility_duration - (pygame.time.get_ticks() - invincibility_timer)
            timer_text = font.render(f'Time Left: {remaining_time // 1000}', True, (255, 0, 0))  # Show remaining time in seconds
            screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))  # Position the timer at the top right

        # Draw visible game timer
        elapsed_time = (pygame.time.get_ticks() - game_start_time) // 1000  # Calculate elapsed time in seconds
        game_timer_text = font.render(f'Time: {elapsed_time}', True, (255, 255, 255))  # Show elapsed time
        screen.blit(game_timer_text, (10, 50))  # Position the game timer at the top left

    else:
        # Game over screen
        game_over_text = font.render('Game Over! Press R to Restart', True, (255, 0, 0))
        score_text = font.render(f'Final Score: {score}', True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # Restart the game
            game_over = False
            obstacles.clear()
            collectibles.clear()  # Clear collectibles on restart
            score = 0
            car_x = SCREEN_WIDTH // 2 - CAR_WIDTH // 2
            car_y = SCREEN_HEIGHT - CAR_HEIGHT - 20
            game_start_time = pygame.time.get_ticks()  # Reset the game start time

    pygame.display.flip()
    clock.tick(FPS)
