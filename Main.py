# Deledan: Guardian of the Verdant Cycle
# VERSÃO FINAL, CORRIGIDA E LEGÍVEL
import pygame
import sys
import random
import math
import numpy as np

# --- INICIALIZAÇÃO E CONSTANTES GLOBAIS ---
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

WIDTH, HEIGHT = 768, 576
TILE_SIZE = 32
MAP_WIDTH, MAP_HEIGHT = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Deledan: Guardian of the Verdant Cycle")
clock = pygame.time.Clock()
FPS = 60

COLORS = {
    'grass': (74, 117, 44), 'dark_grass': (55, 89, 35),
    'tree_top': (46, 93, 34), 'tree_trunk_base': (102, 51, 0), 'tree_trunk_mid': (90, 45, 0),
    'water': (64, 164, 223), 'water_ripple': (100, 184, 240),
    'path': (200, 180, 120),
    'white': (255, 255, 255), 'black': (0, 0, 0),
    'red': (180, 30, 60), 'red_dark': (90, 0, 20),
    'yellow': (230, 200, 0), 'blue': (50, 90, 200), 'skin': (245, 210, 180),
    'cloak': (25, 110, 25), 'life_seed': (120, 220, 80), 'seed': (80, 60, 0),
    'button_bg': (36, 73, 24), 'button_hover': (46, 93, 34)
}

GRASS, TREE, WATER, PATH = 0, 1, 2, 3
solid_tiles = [TREE]
slow_tiles = [WATER]
map_data = []


# --- FUNÇÃO GERADORA DE SOM ---
def generate_sound_array(frequency=440.0, duration=0.1, waveform='square', sample_rate=22050):
    num_samples = int(sample_rate * duration)
    time_array = np.linspace(0., duration, num_samples, endpoint=False)
    if waveform == 'sine':
        wave = np.sin(2 * np.pi * frequency * time_array)
    elif waveform == 'square':
        wave = np.sign(np.sin(2 * np.pi * frequency * time_array))
    elif waveform == 'noise':
        wave = np.random.uniform(-1, 1, size=num_samples)
    else:  # Sawtooth
        wave = 2 * (time_array * frequency - np.floor(0.5 + time_array * frequency))
    envelope = np.linspace(1., 0., num_samples)
    wave *= envelope
    wave = (wave * 32767).astype(np.int16)
    stereo_wave = np.repeat(wave.reshape(num_samples, 1), 2, axis=1)
    return stereo_wave


# --- FUNÇÕES DE DESENHO ---
def draw_grass(s, x, y): pygame.draw.rect(s, COLORS['grass'], (x, y, TILE_SIZE, TILE_SIZE))


def draw_tree(s, x, y):
    pygame.draw.rect(s, COLORS['tree_trunk_base'], (x + 12, y + 16, 8, 16))
    pygame.draw.rect(s, COLORS['tree_trunk_mid'], (x + 13, y + 16, 6, 16))
    pygame.draw.circle(s, COLORS['tree_top'], (x + 16, y + 10), 14)
    pygame.draw.circle(s, COLORS['tree_top'], (x + 8, y + 18), 10)
    pygame.draw.circle(s, COLORS['tree_top'], (x + 24, y + 18), 10)


def draw_water(s, x, y, time):
    pygame.draw.rect(s, COLORS['water'], (x, y, TILE_SIZE, TILE_SIZE))
    ripple = (math.sin(time * 2 + x + y) + 1) / 2
    pygame.draw.circle(s, COLORS['water_ripple'], (x + TILE_SIZE // 2, y + TILE_SIZE // 2), int(ripple * 8), 1)


def draw_path(s, x, y): pygame.draw.rect(s, COLORS['path'], (x, y, TILE_SIZE, TILE_SIZE))


def draw_player(s, x, y, anim_frame, is_invincible, move_direction):
    if is_invincible and pygame.time.get_ticks() % 200 < 100: return
    body_y_offset = 0
    if move_direction != (0, 0): body_y_offset = math.sin(pygame.time.get_ticks() / 100.0 * math.pi * 2) * 1.5
    pygame.draw.rect(s, COLORS['cloak'], (x + 8, y + 8 + body_y_offset, 16, 24))
    pygame.draw.circle(s, COLORS['skin'], (x + 16, y + 12 + body_y_offset), 6)
    leg_y = y + 28 + body_y_offset
    if anim_frame == 0:
        pygame.draw.rect(s, COLORS['blue'], (x + 10, leg_y, 4, 8))
        pygame.draw.rect(s, COLORS['blue'], (x + 18, leg_y + 2, 4, 6))
    else:
        pygame.draw.rect(s, COLORS['blue'], (x + 10, leg_y + 2, 4, 6))
        pygame.draw.rect(s, COLORS['blue'], (x + 18, leg_y, 4, 8))


def draw_seed(s, x, y): pygame.draw.circle(s, COLORS['seed'], (int(x), int(y)), 4)


def draw_enemy(s, x, y, enemy_type):
    color = COLORS['yellow'] if enemy_type == 'erratico' else COLORS['red']
    pygame.draw.circle(s, color, (int(x) + 16, int(y) + 16), 12)
    pygame.draw.circle(s, COLORS['red_dark'], (int(x) + 12, int(y) + 12), 2)
    pygame.draw.circle(s, COLORS['red_dark'], (int(x) + 20, int(y) + 12), 2)
    pygame.draw.line(s, COLORS['red_dark'], (int(x) + 12, int(y) + 20), (int(x) + 20, int(y) + 20), 2)


def draw_powerup(s, x, y):
    pygame.draw.circle(s, COLORS['life_seed'], (x + TILE_SIZE // 2, y + TILE_SIZE // 2), 8)
    pygame.draw.circle(s, COLORS['white'], (x + TILE_SIZE // 2 - 2, y + TILE_SIZE // 2 - 2), 2)


# --- CLASSES DE ENTIDADES DO JOGO ---
class Particle:
    def __init__(self, x, y, color, size, lifespan):
        self.x, self.y, self.color, self.size, self.lifespan = x, y, color, size, lifespan
        self.vx, self.vy = random.uniform(-1, 1), random.uniform(-1, 1)

    def update(self):
        self.x += self.vx;
        self.y += self.vy;
        self.lifespan -= 1;
        self.size = max(0, self.size - 0.1)

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), int(self.size))


class PowerUp:
    def __init__(self, x, y):
        self.x, self.y = x, y;
        self.type = 'health'

    def rect(self):
        return pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)

    def draw(self, surf):
        draw_powerup(surf, self.x, self.y)


class Seed:
    def __init__(self, x, y, direction):
        self.x, self.y = x + 16, y + 16
        self.vx, self.vy = direction[0], direction[1]
        speed = 300
        self.vx *= speed;
        self.vy *= speed
        self.lifespan = 1.5

    def update(self, dt):
        self.x += self.vx * dt;
        self.y += self.vy * dt;
        self.lifespan -= dt

    def rect(self):
        return pygame.Rect(int(self.x) - 3, int(self.y) - 3, 6, 6)

    def draw(self, surf):
        draw_seed(surf, self.x, self.y)


class Player:
    def __init__(self, start_x, start_y):
        self.x, self.y = start_x, start_y
        self.base_speed = 100
        self.alive = True
        self.max_health = 3
        self.health = self.max_health
        self.invincibility_duration = 1.5
        self.invincibility_timer = 0
        self.anim_timer = 0
        self.anim_frame = 0
        self.is_moving = False
        self.last_move_direction = (0, 1)
        self.is_dashing = False
        self.dash_speed = 400
        self.dash_duration = 0.15
        self.dash_timer = 0
        self.dash_cooldown = 1.0
        self.dash_cooldown_timer = 0
        self.dash_direction = (0, 0)
        self.can_shoot = False
        self.shoot_duration = 30
        self.shoot_timer = 0
        self.shoot_cooldown = 0.25
        self.shoot_cooldown_timer = 0

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), TILE_SIZE, TILE_SIZE)

    # REESCRITO PARA CLAREZA
    def update(self, dt, move_direction):
        self.invincibility_timer = max(0, self.invincibility_timer - dt)
        self.shoot_cooldown_timer = max(0, self.shoot_cooldown_timer - dt)
        self.is_moving = (move_direction != (0, 0))
        if self.is_moving:
            self.last_move_direction = move_direction
            self.anim_timer += dt
            if self.anim_timer > 0.15:
                self.anim_timer = 0
                self.anim_frame = 1 - self.anim_frame
        if self.can_shoot:
            self.shoot_timer -= dt
            if self.shoot_timer <= 0:
                self.can_shoot = False

    def activate_shooting(self):
        if not self.can_shoot:
            self.can_shoot = True
            self.shoot_timer = self.shoot_duration

    # REESCRITO PARA CLAREZA
    def move(self, dx, dy, dt):
        self.dash_cooldown_timer = max(0, self.dash_cooldown_timer - dt)
        speed = self.base_speed * (0.5 if self.get_tile() in slow_tiles else 1.0)

        if self.is_dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.is_dashing = False
            dx, dy = self.dash_direction
            speed = self.dash_speed

        self.x += dx * speed * dt
        if not self.is_valid_pos(self.rect()):
            self.x -= dx * speed * dt

        self.y += dy * speed * dt
        if not self.is_valid_pos(self.rect()):
            self.y -= dy * speed * dt

        if self.x < -TILE_SIZE / 2:
            self.x = WIDTH - TILE_SIZE / 2; return 'wrap'
        elif self.x >= WIDTH:
            self.x = -TILE_SIZE / 2; return 'wrap'
        if self.y < -TILE_SIZE / 2:
            self.y = HEIGHT - TILE_SIZE / 2; return 'wrap'
        elif self.y >= HEIGHT:
            self.y = -TILE_SIZE / 2; return 'wrap'

        return None

    def is_valid_pos(self, rect):
        points_to_check = [rect.topleft, (rect.right - 1, rect.top), (rect.left, rect.bottom - 1),
                           (rect.right - 1, rect.bottom - 1)]
        for x, y in points_to_check:
            tx, ty = int(x // TILE_SIZE), int(y // TILE_SIZE)
            if not (0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT): continue
            if map_data[ty][tx] in solid_tiles: return False
        return True

    def perform_dash(self, dx, dy):
        if self.dash_cooldown_timer <= 0 and (dx != 0 or dy != 0):
            self.is_dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown_timer = self.dash_cooldown
            norm = math.sqrt(dx * dx + dy * dy) if (dx * dx + dy * dy) > 0 else 1
            self.dash_direction = (dx / norm, dy / norm)

    def take_damage(self, amount):
        if self.invincibility_timer <= 0:
            self.health -= amount
            self.invincibility_timer = self.invincibility_duration
            if self.health <= 0:
                self.health = 0
                self.alive = False
            return True
        return False

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def draw(self, surf):
        draw_player(surf, int(self.x), int(self.y), self.anim_frame, self.invincibility_timer > 0,
                    self.last_move_direction)

    def get_tile(self):
        center_x, center_y = self.rect().center
        tx, ty = int(center_x // TILE_SIZE), int(center_y // TILE_SIZE)
        return map_data[ty][tx] if 0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT else GRASS


class Enemy:
    def __init__(self, difficulty_scale=1.0):
        self.x, self.y = random.randint(0, WIDTH - TILE_SIZE), random.randint(0, HEIGHT - TILE_SIZE)
        while map_data[int(self.y // TILE_SIZE)][int(self.x // TILE_SIZE)] in solid_tiles:
            self.x, self.y = random.randint(0, WIDTH - TILE_SIZE), random.randint(0, HEIGHT - TILE_SIZE)
        self.speed = random.uniform(30, 50) * difficulty_scale
        self.type = random.choice(['perseguidor', 'erratico'])
        self.erratic_timer = 0
        self.erratic_direction = (0, 0)
        self.health = 2
        if self.type == 'erratico':
            self.speed *= 1.2
            self.health = 1

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), TILE_SIZE, TILE_SIZE)

    # REESCRITO PARA CLAREZA
    def update(self, dt, target):
        speed = self.speed * (0.5 if self.get_tile() in slow_tiles else 1.0)
        dx, dy = 0, 0
        if self.type == 'perseguidor':
            if target.x > self.x:
                dx = 1
            elif target.x < self.x:
                dx = -1
            if target.y > self.y:
                dy = 1
            elif target.y < self.y:
                dy = -1
        elif self.type == 'erratico':
            self.erratic_timer -= dt
            if self.erratic_timer <= 0:
                self.erratic_timer = random.uniform(0.5, 1.5)
                self.erratic_direction = (random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
            dx, dy = self.erratic_direction
        self.x += dx * speed * dt
        self.y += dy * speed * dt
        self.x = max(0, min(self.x, WIDTH - TILE_SIZE))
        self.y = max(0, min(self.y, HEIGHT - TILE_SIZE))

    def take_damage(self, amount):
        self.health -= amount; return self.health <= 0

    def draw(self, surf):
        draw_enemy(surf, self.x, self.y, self.type)

    def get_tile(self):
        tx, ty = int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)
        return map_data[ty][tx] if 0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT else GRASS


# --- CLASSE PRINCIPAL DO JOGO ---
class Game:
    def __init__(self):
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.story_font = pygame.font.SysFont("Georgia", 22)
        self.button_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.font = pygame.font.SysFont("Arial", 20)
        self.state = 'story_screen'
        self.story_pages = [
            "The wind whispers through the leaves, a mournful song of imbalance.\n\nDeledan, the ancient heartwood, calls to its Guardian.",
            "Awaken, protector. The verdant cycle falters.\n\nRestless shadows stir where life once flourished.",
            "You must navigate the shifting woods, drawing strength from\nits remaining vitality...",
            "...and find a way to restore the harmony before the blight consumes all.",
            "Your journey begins now."
        ]
        self.story_page_index = 0
        self.start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
        self.quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50)
        self.player = None
        self.enemies = []
        self.particles = []
        self.powerups = []
        self.seeds = []
        self.powerup_spawn_timer = 0
        self.survival_time = 0
        self.sounds = {
            'shoot': pygame.sndarray.make_sound(generate_sound_array(660, 0.1, 'square')),
            'player_hit': pygame.sndarray.make_sound(generate_sound_array(220, 0.2, 'sawtooth')),
            'enemy_die': pygame.sndarray.make_sound(generate_sound_array(110, 0.15, 'noise')),
            'pickup': pygame.sndarray.make_sound(generate_sound_array(880, 0.15, 'sine')),
            'dash': pygame.sndarray.make_sound(generate_sound_array(1200, 0.08, 'square')),
            'menu_select': pygame.sndarray.make_sound(generate_sound_array(440, 0.1, 'sine')),
        }
        self.sounds['player_hit'].set_volume(0.5)

    def render_multiline_text(self, surface, text, pos, font, color):
        lines = text.split('\n');
        x, y = pos
        for line in lines:
            line_surface = font.render(line, True, color)
            surface.blit(line_surface, (x - line_surface.get_width() // 2, y))
            y += font.get_linesize()

    def find_safe_spawn_point(self):
        while True:
            tx = random.randint(0, MAP_WIDTH - 1);
            ty = random.randint(0, MAP_HEIGHT - 1)
            if map_data[ty][tx] not in solid_tiles: return tx * TILE_SIZE, ty * TILE_SIZE

    def reset_game(self):
        global map_data;
        map_data = [[random.choice([GRASS, GRASS, GRASS, GRASS, TREE, PATH, WATER]) for _ in range(MAP_WIDTH)] for _ in
                    range(MAP_HEIGHT)]
        start_x, start_y = self.find_safe_spawn_point();
        self.player = Player(start_x, start_y)
        self.enemies = [Enemy() for _ in range(3)];
        self.particles.clear();
        self.powerups.clear();
        self.seeds.clear()
        self.spawn_timer = 0;
        self.spawn_interval = 4;
        self.survival_time = 0;
        self.powerup_spawn_timer = random.uniform(8, 15)
        self.shoot_activated_this_cycle = False

    def regenerate_map(self):
        global map_data;
        map_data = [[random.choice([GRASS, GRASS, GRASS, TREE, PATH, GRASS]) for _ in range(MAP_WIDTH)] for _ in
                    range(MAP_HEIGHT)]
        self.player.x, self.player.y = self.find_safe_spawn_point()

    def update(self, dt, move_direction):
        if self.state != 'game': return
        if not self.player or not self.player.alive: return
        self.player.update(dt, move_direction)
        dx, dy = move_direction
        if self.player.move(dx, dy, dt) == 'wrap': self.regenerate_map()
        for e in self.enemies[:]:
            e.update(dt, self.player)
            if e.rect().colliderect(self.player.rect()):
                if self.player.take_damage(1):
                    self.sounds['player_hit'].play()
                    for _ in range(10): self.particles.append(
                        Particle(self.player.x + 16, self.player.y + 16, COLORS['red'], random.randint(2, 5), 30))
            for seed in self.seeds[:]:
                if e.rect().colliderect(seed.rect()):
                    self.sounds['enemy_die'].play()
                    for _ in range(5): self.particles.append(
                        Particle(seed.x, seed.y, COLORS['seed'], random.randint(2, 4), 15))
                    if e.take_damage(1):
                        for _ in range(15): self.particles.append(
                            Particle(e.x + 16, e.y + 16, COLORS['yellow'], random.randint(2, 6), 25))
                        if e in self.enemies: self.enemies.remove(e)
                    if seed in self.seeds: self.seeds.remove(seed)
        self.powerup_spawn_timer -= dt
        if self.powerup_spawn_timer <= 0:
            px, py = random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1)
            if map_data[py][px] not in solid_tiles and map_data[py][px] not in slow_tiles:
                self.powerups.append(PowerUp(px * TILE_SIZE, py * TILE_SIZE))
                self.powerup_spawn_timer = random.uniform(10, 20)
        for p in self.powerups[:]:
            if self.player.rect().colliderect(p.rect()):
                self.sounds['pickup'].play()
                self.player.heal(1)
                for _ in range(15): self.particles.append(
                    Particle(p.x + 16, p.y + 16, COLORS['life_seed'], random.randint(3, 6), 40))
                self.powerups.remove(p)
        self.spawn_timer += dt;
        self.survival_time += dt
        if int(self.survival_time) > 0 and int(
                self.survival_time) % 30 == 0 and not self.player.can_shoot and not self.shoot_activated_this_cycle:
            self.player.activate_shooting();
            self.shoot_activated_this_cycle = True
        if int(self.survival_time) % 30 != 0: self.shoot_activated_this_cycle = False
        if self.spawn_timer >= self.spawn_interval:
            difficulty = 1 + (self.survival_time // 15);
            self.enemies.append(Enemy(difficulty_scale=difficulty));
            self.spawn_timer = 0
        for seed in self.seeds[:]:
            seed.update(dt)
            if seed.lifespan <= 0: self.seeds.remove(seed)
        for p in self.particles[:]:
            p.update()
            if p.lifespan <= 0: self.particles.remove(p)

    def draw(self):
        if self.state == 'story_screen':
            self.draw_story_screen()
        elif self.state == 'main_menu':
            self.draw_main_menu()
        elif self.state == 'game':
            self.draw_game()

    def draw_story_screen(self):
        screen.fill(COLORS['black'])
        self.render_multiline_text(screen, self.story_pages[self.story_page_index], (WIDTH // 2, HEIGHT // 3),
                                   self.story_font, COLORS['white'])
        prompt_text = self.font.render("Press [ENTER] to continue...", True, COLORS['yellow'])
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT - 100))

    def draw_main_menu(self):
        screen.fill(COLORS['dark_grass'])
        title_text = self.title_font.render("Deledan", True, COLORS['white'])
        subtitle_text = self.button_font.render("Guardian of the Verdant Cycle", True, COLORS['white'])
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, HEIGHT // 4 + 60))
        mouse_pos = pygame.mouse.get_pos()
        start_color = COLORS['button_hover'] if self.start_button.collidepoint(mouse_pos) else COLORS['button_bg']
        pygame.draw.rect(screen, start_color, self.start_button, border_radius=10)
        start_text = self.button_font.render("Start Game", True, COLORS['white'])
        screen.blit(start_text, (self.start_button.centerx - start_text.get_width() // 2,
                                 self.start_button.centery - start_text.get_height() // 2))
        quit_color = COLORS['button_hover'] if self.quit_button.collidepoint(mouse_pos) else COLORS['button_bg']
        pygame.draw.rect(screen, quit_color, self.quit_button, border_radius=10)
        quit_text = self.button_font.render("Quit", True, COLORS['white'])
        screen.blit(quit_text, (self.quit_button.centerx - quit_text.get_width() // 2,
                                self.quit_button.centery - quit_text.get_height() // 2))

    def draw_game(self):
        self.draw_map()
        for p in self.powerups: p.draw(screen)
        for e in self.enemies: e.draw(screen)
        for seed in self.seeds: seed.draw(screen)
        for p in self.particles: p.draw(screen)
        if self.player and self.player.alive: self.player.draw(screen)
        self.draw_ui()
        if self.player and not self.player.alive:
            dead_text = "Game Over - Press R to Restart"
            dead_surf = self.font.render(dead_text, True, COLORS['white'])
            screen.blit(dead_surf, (WIDTH // 2 - dead_surf.get_width() // 2, HEIGHT // 2))

    def draw_map(self):
        time = pygame.time.get_ticks() / 1000.0
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                t = map_data[y][x];
                px, py = x * TILE_SIZE, y * TILE_SIZE
                if t == GRASS:
                    draw_grass(screen, px, py)
                elif t == TREE:
                    draw_tree(screen, px, py)
                elif t == WATER:
                    draw_water(screen, px, py, time)
                elif t == PATH:
                    draw_path(screen, px, py)

    def draw_ui(self):
        if not self.player: return
        time_text = f"Time: {int(self.survival_time)}s"
        screen.blit(self.font.render(time_text, True, COLORS['white']), (10, 10))
        dash_text = f"Dash: {'READY' if self.player.dash_cooldown_timer <= 0 else str(round(self.player.dash_cooldown_timer, 1))}"
        dash_color = COLORS['yellow'] if self.player.dash_cooldown_timer <= 0 else COLORS['white']
        screen.blit(self.font.render(dash_text, True, dash_color), (10, 35))
        health_bar_bg = pygame.Rect(WIDTH - 110, 10, 100, 20)
        pygame.draw.rect(screen, COLORS['red_dark'], health_bar_bg)
        health_ratio = self.player.health / self.player.max_health
        health_bar_fg = pygame.Rect(WIDTH - 110, 10, 100 * health_ratio, 20)
        pygame.draw.rect(screen, COLORS['red'], health_bar_fg)
        pygame.draw.rect(screen, COLORS['white'], health_bar_bg, 2)
        if self.player.can_shoot:
            shoot_text = f"SHOOT READY (F) [{int(self.player.shoot_timer)}s]"
            shoot_surf = self.font.render(shoot_text, True, COLORS['yellow'])
            screen.blit(shoot_surf, (WIDTH // 2 - shoot_surf.get_width() // 2, 10))


# --- LOOP PRINCIPAL DO JOGO ---
def main():
    game = Game()
    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        move_direction = [0, 0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

            if game.state == 'story_screen':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game.sounds['menu_select'].play()
                    game.story_page_index += 1
                    if game.story_page_index >= len(game.story_pages):
                        game.state = 'main_menu'

            elif game.state == 'main_menu':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if game.start_button.collidepoint(event.pos):
                        game.sounds['menu_select'].play()
                        game.reset_game()
                        game.state = 'game'
                    if game.quit_button.collidepoint(event.pos):
                        running = False

            elif game.state == 'game' and game.player:
                if event.type == pygame.KEYDOWN:
                    if not game.player.alive and event.key == pygame.K_r:
                        game.reset_game()
                    elif game.player.alive:
                        keys = pygame.key.get_pressed()
                        temp_move = [0, 0]
                        if keys[pygame.K_w]: temp_move[1] -= 1
                        if keys[pygame.K_s]: temp_move[1] += 1
                        if keys[pygame.K_a]: temp_move[0] -= 1
                        if keys[pygame.K_d]: temp_move[0] += 1

                        if event.key == pygame.K_SPACE:
                            game.player.perform_dash(temp_move[0], temp_move[1])
                            game.sounds['dash'].play()
                        elif event.key == pygame.K_f and game.player.can_shoot and game.player.shoot_cooldown_timer <= 0:
                            game.seeds.append(Seed(game.player.x, game.player.y, game.player.last_move_direction))
                            game.player.shoot_cooldown_timer = game.player.shoot_cooldown
                            game.sounds['shoot'].play()

        if game.state == 'game' and game.player and game.player.alive:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]: move_direction[1] -= 1
            if keys[pygame.K_s]: move_direction[1] += 1
            if keys[pygame.K_a]: move_direction[0] -= 1
            if keys[pygame.K_d]: move_direction[0] += 1

        game.update(dt, tuple(move_direction))

        screen.fill(COLORS['black'])
        game.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()