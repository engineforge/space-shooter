from pygame import *
from random import randint
from time import sleep

lost = 0
score = 0
goal = 200
max_lost = 10
max_health=100
health = 100
damage_per_hit = 10

fire_cooldown = 0
fire_delay = 150

window_width = 1280
window_height = 720

class GameSprite(sprite.Sprite):
        def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
           super().__init__()
           self.image = transform.scale(image.load(player_image), (size_x, size_y))
           self.speed = player_speed
           self.rect = self.image.get_rect()
           self.rect.x = player_x
           self.rect.y = player_y
        
        def reset(self):
            window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < window_width - self.rect.width:
            self.rect.x += self.speed
        if (keys[K_UP] or keys[K_w]) and self.rect.y > 5:
            self.rect.y -= self.speed
        if (keys[K_DOWN] or keys[K_s]) and self.rect.y < window_height - self.rect.width:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet("data/bullet_player.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > window_height:
            self.rect.x = randint(80, window_width - 80)
            self.rect.y = 0

class Enemy_Ship(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > window_height:
            self.rect.x = randint(80, window_width - 80)
            self.rect.y = 0
            lost = lost + 1
    def fire(self):
        enemy_bullet = Bullet("data/bullet_enemy.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        enemy_bullets.add(enemy_bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()
        if self.rect.y > window_height:
            self.kill()

class Medkit(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = image.load("data/medkit.png")
        self.image = transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))

def wait_for_start():
    waiting = True
    while waiting:
        for e in event.get():
            if e.type == QUIT:
                quit()
            elif e.type == KEYDOWN:
                if e.key == K_e:
                    waiting = False

        window.fill((0, 0, 0))
        font_big = font.SysFont(None, 60)
        text = font_big.render("Press E to start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)
        display.update()
        clock.tick(30)

def show_end_screen(result_surface):
    if not display.get_init():
        return 
    
    window.blit(background, (0, 0))
    all_enemies.draw(window)
    bullets.draw(window)
    medkits.draw(window)
    ship.reset()
    window.blit(text_lost, (10, 50))
    draw_progress_bar(surface=window, x=10, y=10, current_value=score, max_value=goal)
    window.blit(health_icon, (10, 78))
    draw_health_bar(surface=window, x=50, y=90, current_health=health, max_health=max_health)

    window.blit(result_surface, (over_font_center_x, over_font_center_y))

    display.update()

    waiting = True
    while waiting:
        for e in event.get():
            if e.type == QUIT:
                waiting = False
                quit()
                return 
            elif e.type == KEYDOWN:
                waiting = False

        clock.tick(30)

def get_non_overlapping_x(existing_sprites, width, margin=80, attempts=100):
    for _ in range(attempts):
        x = randint(margin, window_width - margin - width)
        overlap = False
        for sprite in existing_sprites:
            if abs(sprite.rect.x - x) < width:
                overlap = True
                break
        if not overlap:
            return x
    return randint(margin, window_width - margin - width)

def draw_progress_bar(surface, x, y, current_value, max_value, width=300, height=25,
                      fill_color=(0, 255, 0), bg_color=(0, 0, 0), border_color=(255, 255, 255)):
    progress = current_value / max_value
    fill_width = int(width * progress)
    draw.rect(surface, bg_color, (x, y, width, height))
    draw.rect(surface, fill_color, (x, y, fill_width, height))
    draw.rect(surface, border_color, (x, y, width, height), 2)

def draw_health_bar(surface, x, y, current_health, max_health, width=200, height=10, border_radius=5):
    ratio = current_health / max_health
    draw.rect(surface, (255, 0, 0), (x, y, width, height), border_radius=border_radius)

    filled_width = int(width * ratio)
    if filled_width > 0:
        draw.rect(surface, (255, 165, 0), (x, y, filled_width, height), border_radius=border_radius)

enemys = sprite.Group()
enemys2 = sprite.Group()
all_enemies = sprite.Group()
all_sprites = sprite.Group()
medkits = sprite.Group()

for i in range(1, 6):
    x_pos = get_non_overlapping_x(all_enemies, 80)
    enemy = Enemy("data/asteroid.png", x_pos, -40, 80, 50, randint(1,3))
    enemys.add(enemy)
    all_enemies.add(enemy)

for j in range(1, 6):
    x_pos = get_non_overlapping_x(all_enemies, 80)
    enemy2 = Enemy_Ship("data/ufo.png", x_pos, -40, 80, 50, 1)
    enemys2.add(enemy2)
    all_enemies.add(enemy2)


enemy_bullets = sprite.Group()

bullets = sprite.Group()

ship = Player("data/ship.png", 300, 300, 80, 50, 10)

image_back = "data/galaxy.jpg"

game_icon = image.load("data/ship.png")
health_icon = image.load("data/health_big.png")
health_icon = transform.scale(health_icon, (32, 32))
display.set_icon(game_icon)

window = display.set_mode((window_width, window_height))
display.set_caption("Space Shooter")
background = transform.scale(image.load(image_back), (window_width, window_height))

clock = time.Clock()

run = True
finish = False

font.init()
font1 = font.SysFont(None, 80)
font2 = font.SysFont(None, 36)
victory_font = font1.render("VICTORY", True, (0, 255, 0))
victory_font_width, victory_font_height = victory_font.get_size()
victory_font_center_x = (window_width - victory_font_width) // 2
victory_font_center_y = (window_height - victory_font_height) // 2

over_font = font1.render("GAME OVER", True, (180, 0, 0))
over_font_width, over_font_height = over_font.get_size()
over_font_center_x = (window_width - over_font_width) // 2
over_font_center_y = (window_height - over_font_height) // 2

wait_for_start()

mixer.init()
mixer.music.load("data/Soulbringer - Space Blockbuster.mp3")
mixer.music.play()
fire_sound = mixer.Sound("data/fire.ogg")

while run:
    for e in event.get():
        if e.type == QUIT:
           run = False

    if not finish: 
        keys = key.get_pressed()

        if keys[K_SPACE] and fire_cooldown == 0:
            fire_sound.play()
            ship.fire()
            fire_cooldown = fire_delay

        if fire_cooldown > 0:
            fire_cooldown -= clock.get_time()
        if fire_cooldown < 0:
            fire_cooldown = 0
        
        window.blit(background, (0, 0))
        ship.update()
        ship.reset()
        bullets.update()
        bullets.draw(window)
        enemys.update()
        enemys.draw(window)
        enemys2.update()
        enemys2.draw(window)
        enemy_bullets.update()
        enemy_bullets.draw(window)
        medkits.draw(window)
        
        for enemy in enemys2:
            if randint(1, 300) == 1:
                enemy.fire()

        draw_progress_bar(surface=window, x=10, y=10, current_value=score, max_value=goal)
    
        text_lost = font2.render(f"Skipped: {lost}/10", True, (255, 255, 255))
        window.blit(text_lost, (10, 50))

        window.blit(health_icon, (10, 78))
        draw_health_bar(surface=window, x=50, y=90, current_health=health, max_health=max_health)

    collides = sprite.groupcollide(enemys, bullets, True, True)
    for enemy in collides:
        x, y = enemy.rect.center

        if randint(1, 100) <= 3:
            medkit = Medkit(x, y)
            medkits.add(medkit)
            all_sprites.add(medkit)

        new_enemy = Enemy("data/asteroid.png", randint(80, window_width - 80), -40, 80, 50, randint(1,3))
        enemys.add(new_enemy)
        all_sprites.add(new_enemy)

    collides2 = sprite.groupcollide(enemys2, bullets, True, True)
    for k in collides2:
        score += 1
        enemy2 = Enemy_Ship("data/ufo.png",randint(80, window_width -80), -40 ,80, 50, 1)
        enemys2.add(enemy2)

    if score == goal:
        finish = True
        show_end_screen(victory_font)

    if lost == max_lost:
        finish = True
        show_end_screen(over_font)

    hit_enemies = sprite.spritecollide(ship, enemys, True)
    for _ in hit_enemies:
        health -= damage_per_hit
        enemy = Enemy("data/asteroid.png", randint(80, window_width - 80), -40, 80, 50, randint(1,3))
        enemys.add(enemy)
        if health <= 0:
            health = 0
            finish = True
            show_end_screen(over_font)

    hit_enemy_ships = sprite.spritecollide(ship, enemys2, True)
    for _ in hit_enemy_ships:
        health -= damage_per_hit
        enemy2 = Enemy_Ship("data/ufo.png", randint(80, window_width - 80), -40, 80, 50, 1)
        enemys2.add(enemy2)
        if health <= 0:
            health = 0
            finish = True
            show_end_screen(over_font)

    hit_bullets = sprite.spritecollide(ship, enemy_bullets, True)
    if hit_bullets:
        health -= damage_per_hit * len(hit_bullets)
    if health <= 0:
        health = 0
        finish = True
        show_end_screen(over_font)
    
    medkit_hits = sprite.spritecollide(ship, medkits, True)
    for medkit in medkit_hits:
        health += 25
        if health > max_health:
            health = max_health

    clock.tick(60)
    display.update()