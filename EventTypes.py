import pygame

GREETING = pygame.USEREVENT + 1
SHAPES = pygame.USEREVENT + 2
SERVER_SEND_SHAPE = pygame.USEREVENT + 3
CLIENT_SEND_SHAPE = pygame.USEREVENT + 4
CLIENT_CREATE_SHAPE = pygame.USEREVENT + 5
SERVER_DELETE_SHAPE = pygame.USEREVENT + 6
CLIENT_CHANGE_SHAPE = pygame.USEREVENT + 7