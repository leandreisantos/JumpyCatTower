import pygame

class Player():
    def __init__(self,x,y,character_image):
        self.image = pygame.transform.scale(character_image, (100, 100))
        self.width = 50
        self.heigth = 70
        self.rect = pygame.Rect(0,0,self.width,self.heigth)
        self.rect.center = (x,y)
        self.vel_y = 0;
        self.flip = False
        self.onGround = True
        self.jumpCount = 0

    def move(self,speed,jump_fx,gravity,SCREEN_WIDTH,platform_group,SCROLL_THRESH,rightToMove):
        #reset var
        scroll = 0
        dx = 0
        dy = 0

        #process keypresses
        if rightToMove:
            key = pygame.key.get_pressed()
            if key[pygame.K_a]:
                dx = -speed
                self.flip = False
            if key[pygame.K_d]:
                dx = speed
                self.flip = True
            if key[pygame.K_SPACE] and self.jumpCount == 0:
                self.vel_y = -18
                self.jumpCount+=1
                jump_fx.play()
        #gravity
        self.vel_y += gravity
        dy += self.vel_y

        #limit player don't go off the edge of the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        #check collision to platforms
        for platform in platform_group:
            #collision in y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.heigth):
                #check if above platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = 0
                        self.jumpCount = 0


        #check collision with ground
        #if self.rect.bottom + dy > SCREEN_HEIGHT:
            #dy = 0
            #self.vel_y = 0
        
        #check if the player has bounced to the top
        if self.rect.top <= SCROLL_THRESH:
           #if player is jumping
           if self.vel_y < 0:
               scroll = -dy

        #update reactangle position
        self.rect.x +=dx
        self.rect.y +=dy +scroll

        #update mask
        self.mask = pygame.mask.from_surface(self.image)

        return scroll

    def draw(self,screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x-20, self.rect.y-15))
        #pygame.draw.rect(screen, WHITE, self.rect, 2)