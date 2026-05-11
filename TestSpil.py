import pygame
import random
import sys
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_desktop_sizes()[0]
print(SCREEN_WIDTH,SCREEN_HEIGHT)
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
        
        for i in range(3):
            for j in range(3):
                pass
        self.sprite = pygame.transform.scale(pygame.image.load("space_bg.png").convert_alpha(),(self.width,self.height))
        #self.sprite = pygame.Surface((self.width,self.height))
        '''
        for i in range(self.width):
            for j in range(self.height):
                self.sprite.set_at((i,self.height-j),(255/self.width*i,0,255/self.height*j))
        '''

# Player class
class Player:
    def __init__(self, x: int, y: int):
        self.img_default = pygame.transform.scale(pygame.image.load("player_sprite_default.png").convert_alpha(), (64, 64))
        self.img_big = pygame.transform.scale(pygame.image.load("player_sprite_big.png").convert_alpha(), (64, 64))

        self.img = self.img_default
        self.rect = self.img.get_rect(center=(x, y))

        self.vel = pygame.Vector2(0, 0)
        self.speed_increment = 100
        self.max_speed = 300
        self.drag = 0.8
        self.diagonal_speed = int(math.sqrt(self.max_speed/2))
        '''
        for i in range(0,self.width+1):
            for j in range(0,self.height+1):
                self.surface.set_at((i,self.height-j),(0,255/self.width*i,255/self.height*j))
        '''
    def update(self,world,dt):
        self.vel.x = max(min(self.vel.x,self.max_speed),-self.max_speed)
        self.vel.y = max(min(self.vel.y,self.max_speed),-self.max_speed)

        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        
        self.vel.x *= self.drag
        self.vel.y *= self.drag
        
        
        self.rect.x = min(max(0,self.rect.x), world.width -self.rect.height)
        self.rect.y = min(max(0,self.rect.y), world.height-self.rect.height)

        #print(self.vel_x,self.vel_y)

class Bullet():
    def __init__(self,x,y):
        self.img = pygame.transform.scale(pygame.image.load("laser.png").convert_alpha(), (64, 64))
        self.rect = self.img.get_rect(center=(x,y))


class Big_bullet():
    def __int__(self,x,y):
        self.img = pygame.transform.scale(pygame.image.load("laser_big.png").convert_alpha(), (64, 64))
        self.rect = self.img.get_rect(center=(x,y))
        
class Bullet:
    def __init__(self, x, y, direction):
        self.pos = pygame.Vector2(x, y)
        self.direction = direction.normalize()
        self.speed = 600
        self.next = None
        self.rect = pygame.Rect(x,y,5,5)

class BulletList:
    def __init__(self):
        self.head = None

    def add(self, x, y, direction):
        new_bullet = Bullet(x, y, direction)

        new_bullet.next = self.head
        self.head = new_bullet
    
    def update(self, dt, world_width, world_height):
        current = self.head
        prev = None

        while current:
            # Move bullet
            current.pos += current.direction * current.speed * dt

            # Remove if off screen
            if (current.pos.x < 0 or current.pos.x > world_width or
                current.pos.y < 0 or current.pos.y > world_height):

                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next

                current = current.next
                continue

            prev = current
            current = current.next

    def draw(self, world):
        current = self.head

        while current:
            pygame.draw.circle(world.surface, (255, 200, 50),
                               (int(current.pos.x), int(current.pos.y)), 5)

            current = current.next

class Enemy():
    def __init__(self,x,y):
        
        self.x = x
        self.y = y

        self.vel_x = 0
        self.vel_y = 0

        self.max_speed = 300

        self.surface = pygame.Surface((50,50))

        self.surface.fill("white")

        for i in range(50):
            for j in range(50):
                self.surface.set_at((i,49-j),(255/50*i,255/50*j,0))
    
    def update(self,player,dt,world):

        dx = self.x - (player.rect.x)
        dy = self.y - (player.rect.y) 

        vel_x = min(max(-self.max_speed,int((dx)*5)), self.max_speed)
        vel_y = min(max(-self.max_speed,int((dy)*5)), self.max_speed)

        self.x -= vel_x*dt
        self.y -= vel_y*dt

        #self.rect.x = min(max(0,self.rect.x), world.width -self.rect.width)
        #self.rect3.y = min(max(0,self.rect.y), world.height -self.rect.height)


class Camera():
    def __init__(self,player_x:int,player_y:int):
        
        self.rect = pygame.Rect(player_x - SCREEN_WIDTH//2, player_y-SCREEN_HEIGHT//2,
                                SCREEN_WIDTH,SCREEN_HEIGHT)
        #self.vel_x = 0
        #self.vel_y = 0
        self.speed_increment = 150
        self.drag = 0.8
        self.max_follow_distance = 1/(0.2)


    def update(self,player_x:int,player_y:int,world,dt):

        dx = self.rect.x - (player_x - SCREEN_WIDTH//2)
        dy = self.rect.y - (player_y - SCREEN_HEIGHT//2)  

        self.rect.x -= int(dx*self.max_follow_distance)*dt
        self.rect.y -= int(dy*self.max_follow_distance)*dt

        self.rect.x = min(max(0,self.rect.x), world.width -self.rect.width)
        self.rect.y = min(max(0,self.rect.y), world.height -self.rect.height)



        #-------------------------------------------
        '''
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
        '''
        #---------------------------------------------

        
        
        #---camera locked to player
        #self.rect.x = player_x - SCREEN_WIDTH//2
        #self.rect.y = player_y - SCREEN_HEIGHT//2

def draw_text(text,x,y,world):
    world.surface.blit(font.render(f"{round(text,2)}",1,"black"),(x,y))

# Game loop

def main():
    last_time=time.time()
    world = World()
    
    player = Player(world.width//2, world.height//2)
    camera = Camera(player_x=player.rect.x,player_y=player.rect.y)
    bullets = BulletList()
    running = True

    player_moving = False

    enemies = []
    enemy_spawn_timer = 0
    enemy_spawn_cooldown = 1
    enemy_spawn_locations=[(0,0),(world.width,0),(0,world.height),(world.width,world.height)]
    deg = 0 
    while running:

        clock.tick(60)

        dt = time.time()-last_time

        last_time = time.time()

        # Event handling

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        

        if enemy_spawn_timer >= enemy_spawn_cooldown:
            enemy_spawn_timer = 0
            location = random.randint(0,3)
            enemies.append(Enemy(enemy_spawn_locations[location][0],enemy_spawn_locations[location][1]))

        enemy_spawn_timer += 1*dt
        enemies_to_remove = []

#---------Player input--------------
        player.moving = 0

        if keys[pygame.K_w]:
            player.vel.y -= player.speed_increment*dt
            player.moving += 1

        if keys[pygame.K_s]:
            player.vel.y += player.speed_increment*dt
            player.moving += 1

        if keys[pygame.K_a]:
            player.vel.x -= player.speed_increment*dt
            player.moving += 1

        if keys[pygame.K_d]:
            player.vel.x += player.speed_increment*dt
            player.moving += 1

        if keys[pygame.K_e]:
            clock.tick(30)
       
        
        if player.moving > 1:
            player.vel.x = max(min(player.vel.x,player.diagonal_speed),-player.diagonal_speed)
            player.vel.y = max(min(player.vel.y,player.diagonal_speed),-player.diagonal_speed)
        
        mx, my = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:  # left click
            
            
            direction = pygame.Vector2(camera.rect.x+mx,camera.rect.y+my) - player.rect.center

            bullets.add(player.rect.centerx, player.rect.centery, direction)

#------------------------------------
        

        dx = player.rect.centerx - (mx+camera.rect.x)
        dy = player.rect.centery - (my+camera.rect.y)
        '''
        angle = -math.degrees(math.atan2(dy, dx))
        rotated_img = pygame.transform.rotate(player.img, angle)
        new_rect = rotated_img.get_rect(center=player.rect.center)
        player.rect=new_rect
        '''

        angle = -math.degrees(math.atan2(dy, dx))+90

        rotated = pygame.transform.rotate(player.img, angle)
        rect = rotated.get_rect(center=player.rect.center)

#--------------Draw everything----------------
        

        world.surface.blit(world.sprite,(0,0))
        
        #world.surface.blit(player.img,player.rect)
        draw_text(angle,player.rect.x-200,player.rect.y-100,world)
        draw_text(mx,player.rect.x-200,player.rect.y-200,world)
        world.surface.blit(rotated, rect)
        player.update(world,dt)

        camera.update(player.rect.x+player.rect.width//2, player.rect.y+player.rect.height//2, world, dt)
        
        
        bullets.update(dt, world.width, world.height)
        bullets.draw(world)


        
        for enemy in enemies:
            current = bullets.head
            while current:
                if current.rect.colliderect(enemy.surface.get_rect(topleft=(enemy.x,enemy.y))):
                    enemies_to_remove.append(enemy)
                current = current.next

            enemy.update(player,dt,world)
            world.surface.blit(enemy.surface,(enemy.x,enemy.y))

        for enemy in enemies:
            if enemy in enemies_to_remove:
                enemies.remove(enemy)
        
        screen.blit(world.surface,(0,0),camera.rect)
        
        #print(f"PX: {player.vel_x}, PY: {player.vel_y}")
        #print(f"CX: {camera.vel_x}, CY: {camera.vel_y}")
        
#-----------------------------------------------

#------------Update------------
        pygame.display.flip()
#------------------------------

main()
pygame.quit()
sys.exit()
