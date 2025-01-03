from src import lynxy
import pygame

# initialize pygame stuff
pygame.init()
window = pygame.display.set_mode((1000, 1000))
ONLINE = False

# determine who is first
first = input('1 for first, 2 for second: ') == '1'
if first: print('your color is red')
if not first: print('your color is blue')

# set up host info
host_rect_coord = (10, 500)
host_color = (255, 0, 0) if first else (0, 255, 0)

# set up opponent info
opp_rect_coord = (940, 500)
opp_color = (0, 255, 0) if first else (255, 0, 0)

# connect lynxy client
client = lynxy.Lynxy(bind=True)
print('host is:', client.get_host())
if ONLINE:
    target_ip = input('input target IP: ')
    target_port = int(input('input target port: '))
    client.connect([target_ip, target_port])
    print('connected to target')
else: print('running local')

# set up event for recieving opponent coord
@client.event(lynxy.Constants.Event.ON_MESSAGE)
def message(data: lynxy.Pool.Message):
    global opp_rect_coord
    opp_rect_coord = data.content

# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        host_rect_coord = (host_rect_coord[0], host_rect_coord[1] - 1)
    elif pressed[pygame.K_s]:
        host_rect_coord = (host_rect_coord[0], host_rect_coord[1] + 1)
    window.fill((0, 0, 0))
    pygame.draw.rect(window, host_color, pygame.Rect(host_rect_coord[0], host_rect_coord[1], 50, 150))
    pygame.draw.rect(window, opp_color, pygame.Rect(opp_rect_coord[0], opp_rect_coord[1], 50, 150))
    pygame.display.update()
    if ONLINE: client.send(host_rect_coord)

pygame.quit()