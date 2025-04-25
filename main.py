import pgzrun
import math
import random
from pygame import Rect
from character_class import Character

WIDTH = 1280
HEIGHT = 704
TITLE = "mushroom_collector"
state = "start"
mushroom_count = 0

music_muted = False
frame_index = 0

music.play("bgmusic")
tree_collide = Rect(913,420, 942-913, 638-226)
platforms1 = [
    Rect(112, 608, 271-112, 5),
    Rect(320, 576, 415-320, 5),
    Rect(480, 544, 638-480, 5),
    Rect(704, 576, 736-704, 5),
    Rect(800, 645, 959-800, 5),
    Rect(864, 416, 1245-864, 5),
    Rect(931,510, 1005-931,5)

]
main_menu = Rect(480, 352, 798-480, 448-352)
exit = Rect(1139, 469, 1182-1139, 40)
platforms2 = [Rect(64, 96, 384 - 64, 5),
              Rect(256, 416, 382-256, 5),
              Rect(1121, 97, 1184 - 1121, 5),
              Rect(992, 161, 1052-992, 5),
              Rect(895,257,959-895,5),
              Rect(992, 357, 1056-992, 5),
              Rect(1056,512, 1280-1056, 5)
              ]
over = Rect(450, 416, 830 - 450, 544 - 416)
door11 = Rect(1024, 358, 1064- 1024, 415- 358)


beetle = Character("beetle000", 4, 2)

moving_platform = Rect(448, 417, 576 - 448, 5)

music_button = Actor("musicon", topleft=(640-48, 250+60+10))

shroom1 = Actor("shroom1", topleft=(0, 0))
shroom1_rect = Rect(230, 594, 247-230, 607-594)
shroom2 = Actor("shroom2", topleft=(0, 0))
shroom2_rect = Rect(969, 502, 986-969, 513-502)
star1 = Actor("star1", topleft=(0, 0))
star1_rect = Rect(307, 365, 337-307,395-365)
star2 = Actor("star2", topleft=(0, 0))
star2_rect = Rect(1138, 46, 1171-1138, 76-46)
platform_speed = 2
platform_direction = 1
moving_platformm = Actor("movingplatform2", topleft=(0, 0))
player = Character("tile", 5, 3)
beetle2 = Character("beetle000", 4, 2)


def get_actor_rect(actor):
    return Rect(
        actor.x - 16 ,
        actor.y - 8,
        actor.width - 96,
        actor.height - 48
    )
def get_real_actor_rect(actor):
    return Rect(
        actor.x ,
        actor.y ,
        actor.width ,
        actor.height
    )
def down():
    animate(beetle.actor, tween="linear", duration=2, pos=(700,200), on_finished=up)
def up():
    animate(beetle.actor, tween="linear", duration=2, pos=(700,700), on_finished=down)

def left():
    animate(beetle2.actor, tween="linear", duration=2.5, pos=(200,512), on_finished=right)
def right():
    animate(beetle2.actor, tween="linear", duration=2.5, pos=(1200,512), on_finished=left)
def draw():
  
    screen.clear()
    if state == "start":
        screen.clear()
        screen.blit("mainbg", (0, 0))
        screen.blit("start", (640-168, 250-60))
        music_button.draw()
        
        screen.blit("exit", (640-96, 620))

    elif state == "lvl1":
        screen.clear()
        screen.blit("background", (0, 0))
        screen.blit("midground", (0,0))
        screen.blit("foreground", (0,0))
        screen.blit("tree", (0, 0))
        screen.blit("collison", (0, 0))
        player.draw()
        shroom1.draw()
        shroom2.draw()
        screen.blit("climb", (0, 0))
        screen.blit("door1",(0,0))
        sounds.mosquito.play()
       
        beetle.draw()
        beetle2.draw()
        
        

    elif state == "lvl2":
        sounds.mosquito.stop()
        screen.clear()
        screen.blit("background2", (0, 0))
        screen.blit("midground2", (0,0))
        screen.blit("collison2", (0,0))
        player.draw()
        moving_platformm.draw()
        star1.draw()
        star2.draw()


        
    elif state == "gameover":
        screen.clear()
        screen.blit("mainbg", (0, 0))
        screen.blit("gameover", (0, 0))
        
    elif state == "win":
        screen.clear()
        screen.blit("mainbg", (0, 0))
        screen.blit("congrats", (0, 0))
        
    
def update():
    global moving_platform, platform_direction,mushroom_count,player_rect, state, moving_platformm
    
    moving_platform.x += platform_speed * platform_direction
    moving_platformm.x += 2 * platform_direction

    if moving_platform.right > 1000 or moving_platform.left < 382:
        platform_direction *= -1  
    
    GRAVITY = 1
    
    if not player.on_ground:
        player.vel_y += GRAVITY
        player.actor.y += player.vel_y

    moved = False

    player_rect = get_actor_rect(player.actor)
    beetle_rect = get_real_actor_rect(beetle.actor)
    beetle2_rect = get_real_actor_rect(beetle2.actor)

    if keyboard.left:
        player.actor.x -= player.speed
        player.direction = "l"
        moved = True
    elif keyboard.right:
        player.actor.x += player.speed
        player.direction = "r"
        moved = True
    
    
    player.state = "walk" if moved else "idle"

    if player.state == "walk":
        
        player.timer += 1
        if player.timer >= 10:

            player.timer = 0
            player.frame_index = (player.frame_index + 1) % player.frame_count
            player.actor.image = f"{player.name}walk{player.direction}00{player.frame_index}"


        
    
    if player.state == "idle":
        player.timer += 1
        if player.timer >= 10:
            player.timer = 0           
            player.frame_index = (player.frame_index + 1) % 5
            player.actor.image = f"{player.name}idle00{player.frame_index}"
 
    if player.on_ground:
        player.state = "idle"
     
    if player.actor.colliderect(shroom1_rect) and state == "lvl1":
        sounds.mosquito.stop()
        sounds.toggle.play()
        sounds.mosquito.play()
        mushroom_count += 1
        shroom1.image = "foreground(1)"
        shroom1_rect.x = -100
        shroom1_rect.y = -100
    if player.actor.colliderect(shroom2_rect) and state == "lvl1":
        sounds.mosquito.stop()
        sounds.toggle.play()
        sounds.mosquito.play()
        mushroom_count += 1
        shroom2.image = "foreground(2)"
        shroom2_rect.x = -100
        shroom2_rect.y = -100

    if player_rect.colliderect(tree_collide) and state == "lvl1":
        player.actor.y -= 2

    if player.actor.colliderect(star1_rect) and state == "lvl2":
        sounds.toggle.play()
        mushroom_count += 1
        star1.image = "foreground(1)"
        star1_rect.x = -100
        star1_rect.y = -100

    if player.actor.colliderect(star2_rect) and state == "lvl2":
        sounds.toggle.play()
        mushroom_count += 1
        star2.image = "foreground(1)"
        star2_rect.x = -100
        star2_rect.y = -100

    if player_rect.colliderect(door11) and mushroom_count == 2 and state == "lvl1":
        sounds.mosquito.stop()
        sounds.door_open.play()
        state = "lvl2"
        player.actor.x = 144
        player.actor.y = 63

    if player_rect.colliderect(exit) and mushroom_count == 4 and state == "lvl2":
        state = "win"
        sounds.game_win.play()

    if (player_rect.colliderect(beetle_rect) or player_rect.colliderect(beetle2_rect)) and state == "lvl1":
        sounds.mosquito.stop()
        sounds.error.play()
        state = "gameover"
        
    if player.actor.y > HEIGHT and (state == "lvl1" or state == "lvl2"):
        sounds.mosquito.stop()
        sounds.error.play()
        state = "gameover"


    if beetle.state == "idle":
        
        beetle.timer += 1
        if beetle.timer >= 10:
            beetle.timer = 0           
            beetle.frame_index = (beetle.frame_index + 1) % 4
            beetle.actor.image = f"{beetle.name}idle00{beetle.frame_index}"
    if beetle2.state == "idle":
        beetle2.timer += 1
        if beetle2.timer >= 10:
            beetle2.timer = 0           
            beetle2.frame_index = (beetle2.frame_index + 1) % 4
            beetle2.actor.image = f"{beetle2.name}idle00{beetle2.frame_index}"


    player_rect = get_actor_rect(player.actor)


    player.on_ground = False
    for ground in platforms1:
        if player_rect.colliderect(ground) and player.vel_y >= 0 and state == "lvl1":
            player.actor.y = ground.top - player.actor.height // 2
            player.vel_y = 0
            player.on_ground = True
            break

    for ground in platforms2:
        if player_rect.colliderect(ground) and player.vel_y >= 0 and state == "lvl2":
            player.actor.y = ground.top - player.actor.height // 2
            player.vel_y = 0
            player.on_ground = True
            break
     
    if player_rect.colliderect(moving_platform) and state == "lvl2":
        player.vel_y = 5
        player.on_ground = True
        player.actor.x += 2 * platform_direction


def on_mouse_down(pos):
    global state, music_muted, mushroom_count
    if state == "start":
        if Rect(640-168, 250-60, 336, 120).collidepoint(pos):
            sounds.select.play()
            state = "lvl1"
            shroom1.image = "shroom1"
            shroom1_rect.x = 230
            shroom1_rect.y = 594
            shroom2.image = "shroom2"
            shroom2_rect.x = 969
            shroom2_rect.y = 502
            mushroom_count = 0
            player.actor.x = 144
            player.actor.y = 63
            player.vel_y = 0
            player.on_ground = True
            star1.image = "star1"
            star1_rect.x = 307
            star1_rect.y = 365
            star2.image = "star2"
            star2_rect.x = 1138
            star2_rect.y = 46

        elif Rect(640-48, 250+60+10, 96, 96).collidepoint(pos):
            sounds.select.play()
            if music_muted:
                music_button.image = "musicon"
                music.set_volume(1.0)
                music_muted = False
            else:
                music.set_volume(0)
                music_button.image = "musicoff"
                music_muted = True
        elif Rect(640-96, 620, 192, 60).collidepoint(pos):
            sounds.select.play()
            exit()
    if state == "gameover":
        if over.collidepoint(pos):
            sounds.select.play()
            state = "start"
            player.actor.x = 144
            player.actor.y = 63
            player.vel_y = 0
            player.on_ground = True

    if state == "win":
        if main_menu.collidepoint(pos):
            state = "start"
            player.actor.x = 144
            player.actor.y = 63
            player.vel_y = 0
            player.on_ground = True
            mushroom_count = 0
            shroom1.image = "shroom1"
            shroom1_rect.x = 230
            shroom1_rect.y = 594
            shroom2.image = "shroom2"
            shroom2_rect.x = 969
            shroom2_rect.y = 502
            
def on_key_down(key):
    global state,moved
    if state == "lvl1" or state == "lvl2" or state == "gameover":
        if key == keys.ESCAPE:
            state = "start"
        elif key == keys.LEFT:
            player.actor.x -= player.speed
            player.direction = "left"
            player.state = "walk"
        elif key == keys.RIGHT:
            player.actor.x += player.speed
            player.direction = "right"
            player.state = "walk"
        if key == keys.UP and player.on_ground:
            player.vel_y = -15
            player.on_ground = False
            player.state = "jump"
            moved = True
down()
left()
pgzrun.go()