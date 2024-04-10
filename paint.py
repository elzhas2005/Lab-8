import pygame 

pygame.init()

shapes_drawn = []
clock = pygame.time.Clock()
fps = 60

active_color = (0, 0, 0)
active_shape = 0

width, height = 800, 600

screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Paint")

def draw_interface():
    pygame.draw.rect(screen, 'gray', [0, 0, width, 100])
    pygame.draw.line(screen, 'black', [0, 100], [width, 100])
    rect_button = [pygame.draw.rect(screen, 'black', [10, 10, 80, 80]), 0]
    circle_button = [pygame.draw.rect(screen, 'black', [100, 10, 80, 80]), 1]
    colors = [
        [pygame.draw.rect(screen, (0, 0, 255), [width - 35, 10, 25, 25]), (0, 0, 255)],
        [pygame.draw.rect(screen, (255, 0, 0), [width - 35, 35, 25, 25]), (255, 0, 0)],
        [pygame.draw.rect(screen, (0, 255, 0), [width - 60, 10, 25, 25]), (0, 255, 0)],
        [pygame.draw.rect(screen, (255, 255, 0), [width - 60, 35, 25, 25]), (255, 255, 0)],
        [pygame.draw.rect(screen, (0, 0, 0), [width - 85, 10, 25, 25]), (0, 0, 0)],
        [pygame.draw.rect(screen, (255, 0, 255), [width - 85, 35, 25, 25]), (255, 0, 255)]
    ]
    return colors, [rect_button, circle_button]

def draw_shapes(shapes):
    for shape in shapes:
        if shape[2] == 1:
            pygame.draw.circle(screen, shape[0], shape[1], 15)
        elif shape[2] == 0:
            pygame.draw.rect(screen, shape[0], [shape[1][0] - 15, shape[1][1] - 15, 30, 30])

def draw_current_shape():
    global active_color, active_shape, mouse
    if mouse[1] > 100:
        if active_shape == 0:
            pygame.draw.rect(screen, active_color, [mouse[0] - 15, mouse[1] - 15, 30, 30])
        if active_shape == 1:
            pygame.draw.circle(screen, active_color, mouse, 15)

running = True
while running:
    clock.tick(fps)
    screen.fill('white')
    colors, buttons = draw_interface()
    mouse = pygame.mouse.get_pos()
    draw_current_shape()
    click = pygame.mouse.get_pressed()[0]
    if click and mouse[1] > 100:
        shapes_drawn.append((active_color, mouse, active_shape))
    draw_shapes(shapes_drawn)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for color in colors:
                if color[0].collidepoint(event.pos):
                    active_color = color[1]
            for button in buttons:
                if button[0].collidepoint(event.pos):
                    active_shape = button[1]

    pygame.display.flip()

pygame.quit()