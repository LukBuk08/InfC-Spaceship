import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_desktop_sizes()[0]

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.toggle_fullscreen()
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# World
class World():
    def __init__(self):
        self.width = SCREEN_WIDTH*3
        self.height = SCREEN_HEIGHT*3
        self.surface = pygame.Surface((self.width,self.height))
        
        self.sprite = pygame.transform.scale(pygame.image.load("bg.png").convert_alpha(),(self.width,self.height))
        #self.sprite = pygame.Surface((self.width,self.height))
        '''
        for i in range(self.width):
            for j in range(self.height):
                self.sprite.set_at((i,self.height-j),(255/self.width*i,0,255/self.height*j))
        '''

# Player class
class Player():
    def __init__(self,x:int,y:int,width,height,color):
        
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width,height))
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.speed_increment = 5
        self.max_speed = 10
        self.drag = 0.8

        for i in range(0,self.width+1):
            for j in range(0,self.height+1):
                self.surface.set_at((i,self.height-j),(0,255/self.width*i,255/self.height*j))

class Enemy():
    def __init__(self):
        
        self.x = 100
        self.y = 100

        self.vel_x = 0
        self.vel_y = 0

        self.surface = pygame.Surface((50,50))
        self.surface.fill("white")

        for i in range(50):
            for j in range(50):
                self.surface.set_at((i,49-j),(255/50*i,255/50*j,0))

class Camera():
    def __init__(self,player_x:int,player_y:int):
        
        self.rect = pygame.Rect(player_x - SCREEN_WIDTH//2, player_y-SCREEN_HEIGHT//2,
                                SCREEN_WIDTH,SCREEN_HEIGHT)
        self.vel_x = 0
        self.vel_y = 0
        self.speed_increment = 5
        self.drag = 0.5
        self.max_follow_distance = 20


    def update(self,player_x:int,player_y:int,player_speed):
        
        dx = self.rect.x - (player_x - SCREEN_WIDTH//2)
        dy = self.rect.y - (player_y - SCREEN_HEIGHT//2)  
    
        angle = math.atan2(dx,dy)
        
        if not -self.max_follow_distance < dx < self.max_follow_distance:
            self.vel_x += math.sin(angle) * self.speed_increment
            
        if not -self.max_follow_distance < dy < self.max_follow_distance:
            self.vel_y += math.cos(angle) * self.speed_increment
            

        self.vel_x = max(min(self.vel_x,player_speed),-player_speed)
        self.vel_y = max(min(self.vel_y,player_speed),-player_speed)
        
        self.rect.x -= int(self.vel_x)
        self.rect.y -= int(self.vel_y)

        self.vel_x = self.vel_x*self.drag
        self.vel_y = self.vel_y*self.drag
        
        
    

        
        
       
        #---camera locked to player
        #self.rect.x = player_x - SCREEN_WIDTH//2
        #self.rect.y = player_y - SCREEN_HEIGHT//2

def draw_text(text,x,y,world):
    world.surface.blit(font.render(f"{round(text,2)}",1,"black"),(x,y))

# Game loop

def main():

    world = World()
    enemy = Enemy()
    player = Player(world.width//2, world.height//2,50,50,"red")
    camera = Camera(player_x=player.x,player_y=player.y)

    running = True

    player_moving = False

    while running:
        clock.tick(60)

        # Event handling

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        


#---------Player input--------------
        if keys[pygame.K_w]:
            player.vel_y -= player.speed_increment
            player_moving = True

        if keys[pygame.K_s]:
            player.vel_y += player.speed_increment
            player_moving = True

        if keys[pygame.K_a]:
            player.vel_x -= player.speed_increment
            player_moving = True

        if keys[pygame.K_d]:
            player.vel_x += player.speed_increment
            player_moving = True

        player.vel_x = max(min(player.vel_x,player.max_speed),-player.max_speed)
        player.vel_y = max(min(player.vel_y,player.max_speed),-player.max_speed)

        player.x += player.vel_x
        player.y += player.vel_y
        
        player.vel_x *= player.drag
        player.vel_y *= player.drag
        
        
#------------------------------------

#--------------Draw everything----------------
        

        world.surface.blit(world.sprite,(0,0))
        world.surface.blit(enemy.surface,(enemy.x,enemy.y))
        world.surface.blit(player.surface,(player.x,player.y))

        camera.update(player.x+player.width//2, player.y+player.height//2, player.max_speed)

        screen.blit(world.surface,(0,0),camera.rect)
        
        
#-----------------------------------------------

#------------Update------------
        pygame.display.flip()
#------------------------------

main()
pygame.quit()
sys.exit()
