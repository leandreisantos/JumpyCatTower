#import library
import pygame
import random
import os
from spritesheet import SpriteSheet
from EnemyServices import Enemy
from pygame import mixer
from PlayerServices import Player
from BonusServices import Bonus

#initialise pygame
mixer.init()
pygame.init()

#game window
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Jump Game")

#set frame rate
clock = pygame.time.Clock()
Fps = 60

#load music and sounds
pygame.mixer.music.load('assets/Music/music.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0)
jump_fx  = pygame.mixer.Sound('assets/Music/jump.mp3')
pygame.mixer.music.set_volume(0.3)
death_fx  = pygame.mixer.Sound('assets/Music/death.mp3')
pygame.mixer.music.set_volume(0.2)


#game variables
SCROLL_THRESH = 200
player_speed = 5
gravity = 1
MAX_PLATFORMS = 30
scroll = 0
bg_scroll = 0
midnight_h = 0
day_h = 0
game_over = False
score = 10
fade_counter = 0
steps = 8
choose = True
rigthToMove = True
p_moving = False
choose_option = random.randint(1,2)
choose_ques1 = 1
choose_ques2 = 1
quesIsAdd = False


if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

#define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,59,54)
PANEL = (154,222, 123)

#define font
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)
font_big_gg = pygame.font.SysFont('Lucida Sans', 50)

#load images
character_image= pygame.image.load('assets/mainCharacter.png')
bg_image = pygame.image.load('assets/BackgroundMain.png').convert_alpha()
game_over_image = pygame.image.load('assets/GameOverPage.png').convert_alpha()
game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
#bg_image = pygame.transform.smoothscale(bg_image, screen.get_size())
platform_image = pygame.image.load('assets/platform.jfif').convert_alpha()
sun_image = pygame.image.load('assets/sun.jpg').convert_alpha()
#bird spritesheet
bird_sheet_img = pygame.image.load('assets/bird.png').convert_alpha()
bird_sheet = SpriteSheet(bird_sheet_img)
bonus_img = pygame.image.load('assets/fishBonus.png').convert_alpha()

#questions
ques1 = pygame.image.load('assets/QuestionImage/ques1.png').convert_alpha()
ques2 = pygame.image.load('assets/QuestionImage/ques2.png').convert_alpha()
ques3 = pygame.image.load('assets/QuestionImage/ques3.png').convert_alpha()
ques4 = pygame.image.load('assets/QuestionImage/ques4.png').convert_alpha()
ques5 = pygame.image.load('assets/QuestionImage/ques5.png').convert_alpha()
ques6 = pygame.image.load('assets/QuestionImage/ques6.png').convert_alpha()
ques7 = pygame.image.load('assets/QuestionImage/ques7.png').convert_alpha()
ques8 = pygame.image.load('assets/QuestionImage/ques8.png').convert_alpha()
ques9 = pygame.image.load('assets/QuestionImage/ques9.png').convert_alpha()
ques10 = pygame.image.load('assets/QuestionImage/ques10.png').convert_alpha()
    
#function for outputing text into the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#function draw info panel
def draw_panel():
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(screen,WHITE, (0,30), (SCREEN_WIDTH, 30), 2)
    draw_text('SCORE: ' + str(score), font_small, RED,0,0)

#function for drawing the bg
def draw_bg(bg_scroll):
    screen.blit(bg_image, (0,0+ bg_scroll))
    screen.blit(bg_image, (0,-700+ bg_scroll))

def draw_gameover():
    screen.blit(game_over_image, (0,0))

def draw_question_panel():
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

def show_question(num_image):
    if num_image == 1:
        screen.blit(ques1, (0,0))
    elif num_image == 2:
        screen.blit(ques2, (0,0))
    elif num_image == 3:
        screen.blit(ques3, (0,0))
    elif num_image == 4:
        screen.blit(ques4, (0,0))
    elif num_image == 5:
        screen.blit(ques5, (0,0))
    elif num_image == 6:
        screen.blit(ques6, (0,0))
    elif num_image == 7:
        screen.blit(ques7, (0,0))
    elif num_image == 8:
        screen.blit(ques8, (0,0))
    elif num_image == 9:
        screen.blit(ques9, (0,0))
    elif num_image == 10:
        screen.blit(ques10, (0,0))

#player class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x,y,width,moving,bonus):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 20))
        self.moving = moving
        self.bonus = bonus
        self.move_counter = random.randint(0,50)
        self.direction = random.choice([-1,1])
        self.speed = random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self,scroll):
        #moving platform side to side if it moving
        if self.moving == True:
            self.move_counter +=1
            self.rect.x += self.direction * self.speed

        #change platform direction if it move full
        if self.move_counter >=100 or self.rect.left < 0 or self.rect.right> SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0

        #update platform vertical position
        self.rect.y += scroll

        #check if platform has gone of the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

#INSTANCES
character = Player(SCREEN_WIDTH//2,SCREEN_HEIGHT - 150,character_image)

#create sprite groups
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bonus_group = pygame.sprite.Group()

#create starting flatform
platform = Platform(SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT - 10, SCREEN_WIDTH, False,False)
platform_group.add(platform)
 
def correct():
    fade_counter = 0
    bonus_group.empty()
    choose = True
    score = score*2
    rigthToMove = True
    jump_fx.play() 


#game loop
run = True
while(run):

    clock.tick(Fps)

    if game_over == False:
        scroll = character.move(player_speed,jump_fx,gravity,SCREEN_WIDTH,platform_group,SCROLL_THRESH,rigthToMove)

        #draw background
        bg_scroll += scroll
        if midnight_h == 5:
            if bg_scroll >=710:
                day_h+=1
                bg_image = pygame.image.load('assets/Night.png').convert()
                bird_sheet_img = pygame.image.load('assets/bird.png').convert_alpha()
                bird_sheet = SpriteSheet(bird_sheet_img)
                steps = 8
                bg_scroll = 0
                if day_h == 5:
                    midnight_h = 0
        else:
            if bg_scroll >=710:
                midnight_h+=1
                bg_image = pygame.image.load('assets/Sky.png').convert_alpha()
                bird_sheet_img = pygame.image.load('assets/bird.png').convert_alpha()
                bird_sheet = SpriteSheet(bird_sheet_img)  
                steps = 8  
                bg_scroll = 0
                if midnight_h == 5:
                    day_h = 0
        draw_bg(bg_scroll)

        #draw temp threshhold
        #pygame.draw.line(screen, WHITE, (0, SCROLL_THRESH),(SCREEN_WIDTH, SCROLL_THRESH))
        
        #generate platforms
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(80,100)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(40,80)
            p_type = random.randint(1,2)
            if p_type == 1 and score > 500:
                p_moving = True
            else:
                p_moving = False
            platform = Platform(p_x,p_y,p_w,p_moving,False)
            platform_group.add(platform)

        if len(bonus_group)<1 and p_moving == False and choose_ques1<=5 and choose_ques2<=5:
            bonus = Bonus(bonus_img,p_x+30,p_y-20,False)
            bonus_group.add(bonus)


        #print(len(platform_group))

        #update platform
        platform_group.update(scroll)

        #generate enemies
        if len(enemy_group) == 0 and score >10000:
            enemy = Enemy(SCREEN_WIDTH, 100, bird_sheet, 2, steps)
            enemy_group.add(enemy)
    
        bonus_group.update(scroll,SCREEN_HEIGHT)
       
        #update enemies
        enemy_group.update(scroll,SCREEN_WIDTH)

        #update score
        if scroll > 0:
            score +=scroll

        #draw line  at previous high score
        pygame.draw.line(screen, WHITE, (0,score-high_score+SCROLL_THRESH), (SCREEN_WIDTH,score-high_score+SCROLL_THRESH), 3)
        draw_text('HIGH SCORE '+ str(high_score), font_small,RED, 0, score-high_score+SCROLL_THRESH)
        
        #draw sprites
        platform_group.draw(screen)
        enemy_group.draw(screen)
        character.draw(screen)
        bonus_group.draw(screen)

        #draw panel
        draw_panel()

        #check game over
        if character.rect.top > SCREEN_HEIGHT:
            game_over = True
            death_fx.play()
        #check collision with enemys
        if pygame.sprite.spritecollide(character, enemy_group, False):
            if pygame.sprite.spritecollide(character, enemy_group, False, pygame.sprite.collide_mask):
                game_over = True
                death_fx.play()
        if pygame.sprite.spritecollide(character, bonus_group, False):
            if pygame.sprite.spritecollide(character, bonus_group, False, pygame.sprite.collide_mask):

                if fade_counter < SCREEN_WIDTH:
                    fade_counter+=5
                    for y in range(0,6, 2):
                        pygame.draw.rect(screen, PANEL, (0, y*117, fade_counter, 117))
                        pygame.draw.rect(screen, PANEL, (SCREEN_WIDTH - fade_counter, (y+1)*117, SCREEN_WIDTH, 117))
                else:
                    draw_question_panel()
                    rigthToMove = False
                    scroll = character.move(player_speed,jump_fx,gravity,SCREEN_WIDTH,platform_group,SCROLL_THRESH,rigthToMove)
                    if choose_option == 1 and choose_ques1<=5:
                        if choose_ques1 == 1:
                            show_question(1)
                            key = pygame.key.get_pressed()
                            if key[pygame.K_2]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                score = score*2
                                rigthToMove = True
                                jump_fx.play()
                            if key[pygame.K_1]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                            if key[pygame.K_3]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                        if choose_ques1 == 2:
                            show_question(2)
                            key = pygame.key.get_pressed()
                            if key[pygame.K_2]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                           
                            if key[pygame.K_1]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                score = score*2
                               
                            if key[pygame.K_3]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                 
                        if choose_ques1 == 3:
                            show_question(3)
                            key = pygame.key.get_pressed()
                            if key[pygame.K_2]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                score = score*2
                               
                            if key[pygame.K_1]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                
                            if key[pygame.K_3]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                
                        if choose_ques1 == 4:
                            show_question(4)
                            key = pygame.key.get_pressed()
                            if key[pygame.K_2]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                
                               
                            if key[pygame.K_1]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                            
                            if key[pygame.K_3]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                score = score*2
                                jump_fx.play()
                              
                        if choose_ques1 == 5:
                            show_question(5)
                            key = pygame.key.get_pressed()
                            if key[pygame.K_2]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                
                               
                            if key[pygame.K_1]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                score = score*2
                               
                            if key[pygame.K_3]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                
                                jump_fx.play()
                    if choose_option == 2 and choose_ques2<=5:
                        if choose_ques1 == 1:
                            show_question(6)
                            key = pygame.key.get_pressed()
                            if key[pygame.K_2]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                
                                rigthToMove = True
                                jump_fx.play()
                            if key[pygame.K_1]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                score = score*2
                                jump_fx.play()
                            if key[pygame.K_3]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                        if choose_ques1 == 2:
                            show_question(7)
                            key = pygame.key.get_pressed()
                            if key[pygame.K_2]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                score = score*2

                            if key[pygame.K_1]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                
                               
                            if key[pygame.K_3]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                 
                        if choose_ques1 == 3:
                            show_question(8)
                            key = pygame.key.get_pressed()
                            if key[pygame.K_2]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                
                               
                            if key[pygame.K_1]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                
                            if key[pygame.K_3]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                score = score*2
                                
                        if choose_ques1 == 4:
                            show_question(9)
                            key = pygame.key.get_pressed()
                            if key[pygame.K_2]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                            
                                score = score*2
                            if key[pygame.K_1]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                            
                            if key[pygame.K_3]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                score = score*2
                                jump_fx.play()
                              
                        if choose_ques1 == 5:
                            show_question(10)
                            key = pygame.key.get_pressed()
                            if key[pygame.K_2]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                
                               
                            if key[pygame.K_1]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                jump_fx.play()
                                score = score*2
                               
                            if key[pygame.K_3]:
                                fade_counter = 0
                                bonus_group.empty()
                                choose = True
                                rigthToMove = True
                                score = score*2
                                jump_fx.play()                                
                if fade_counter == 0 and choose_option ==1:
                    choose_ques1+=1
                if fade_counter == 0 and choose_option == 2:
                    choose_ques2+=1
    else:
        goodToRetry = True
        if fade_counter < SCREEN_WIDTH:
            fade_counter+=5
            for y in range(0,6, 2):
                pygame.draw.rect(screen, RED, (0, y*117, fade_counter, 117))
                pygame.draw.rect(screen, RED, (SCREEN_WIDTH - fade_counter, (y+1)*117, SCREEN_WIDTH, 117))
            
        else:
            draw_gameover()
            draw_text(str(score), font_big_gg, WHITE, 220-((len(str(score))-2)*15), 320)
            #update high score
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            if goodToRetry:
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    #reset variables
                    game_over = False
                    score = 0
                    scroll = 0
                    bg_scroll = 0
                    fade_counter = 0
                    #reposition character
                    character.rect.center =(SCREEN_WIDTH//2,SCREEN_HEIGHT - 150)
                    #reset enemies
                    enemy_group.empty()
                    #reset platform
                    platform_group.empty()
                    #reset bonus
                    bonus_group.empty()
                    #create starting flatform
                    platform = Platform(SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT - 10, SCREEN_WIDTH, False,False)
                    platform_group.add(platform)

                    midnight_h = 0
                    day_h = 0
                    bg_image = pygame.image.load('assets/BackgroundMain.png').convert()
                    choose_option = random.randint(1,2)
                    choose_ques1 = 1
                    choose_ques2 = 1

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
    #update display window
    pygame.display.update()        

pygame.quit()
               
