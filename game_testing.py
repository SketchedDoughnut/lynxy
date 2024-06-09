# other imports
import pygame
import random
import time
import threading

# lynxy imports
from src import lynxy as l, lynxy_server as ls

screen_width = 500
screen_height = 500
screen_dimensions = (screen_width, screen_height)

pygame.init()
window = pygame.display.set_mode(screen_dimensions)

def gen_square() -> pygame.Rect:
    width = 50
    height = 50
    x = random.randint(0, screen_width - width)
    y = random.randint(0, screen_height - height)
    rect = pygame.Rect(x, y, width, height)
    return rect

# ONLY FOR THE SERVER MACHINE
def start_server() -> tuple:
    ip, port, token = ls.start_server()
    return ip, port, token

def start_connection(ip):
    success = l.start_client(ip)
    print(f'Connection status: {success}')



def send_rect():
    while True:
        time.sleep(1)
        l.send_msg(rect, rm)

def gen_new():
    global rect
    while True:
        time.sleep(5)
        rect= gen_square()

def recieve_handler():
    while True:
        global rect
        rect = l.message_queue[-1]



###########

# Code for the SENDING

# initialize rect
rect = gen_square()
# start server
ip, port, token = ls.start_server()
# start client
start_connection(ip)
# go into listener mode
l.send_msg('listener')
rm = False
# start threads to send data
threading.Thread(target=lambda:send_rect()).start()
threading.Thread(target=lambda:gen_new()).start()
# start game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        window.fill((0, 0, 0))
        pygame.draw.rect(window, (255, 255, 255), rect)
        pygame.display.update()
pygame.quit()
ls.freeze_server()
l.shutdown_client()

###########

# Code for the RECIEVING

# # initialize rect
# rect = gen_square()
# # start connection
# start_connection(input('-> '))
# # go into listener mode
# l.send_msg('listener')
# rm = False
# # start thread to recieve data
# l.start_client_listener()
# threading.Thread(target=lambda:recieve_handler()).start()
# # start game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         window.fill((0, 0, 0))
#         pygame.draw.rect(window, (255, 255, 255), rect)
#         pygame.display.update()
# pygame.quit()
# l.shutdown_client()