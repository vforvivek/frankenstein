#!/usr/bin/env python3
"""
Will You Be Frankenstien? - Super Mario Style Edition
WEB DEPLOYMENT READY - All async fixes applied
"""

import pygame
import sys
import os
import math
import random
import asyncio  # REQUIRED FOR WEB

# ------------------------- INIT -------------------------
pygame.init()

# Safe audio init
sound_enabled = True
try:
    pygame.mixer.init()
except pygame.error:
    sound_enabled = False
    print("âš ï¸ Audio disabled")

WIDTH, HEIGHT = 1000, 650
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Will You Be Frankenstien? ðŸŽ®ðŸ’•")
CLOCK = pygame.time.Clock()

FONT_BIG = pygame.font.SysFont("arial", 52, bold=True)
FONT_MED = pygame.font.SysFont("arial", 34)
FONT_SMALL = pygame.font.SysFont("arial", 26)
FONT_TINY = pygame.font.SysFont("arial", 20)

# Colors
MARIO_RED = (240, 20, 20)
MARIO_BLUE = (20, 100, 200)
MARIO_GREEN = (40, 200, 60)
MARIO_BROWN = (120, 80, 40)
MARIO_SKIN = (255, 180, 120)
PINK_DARK = (140, 20, 90)
PINK = (220, 120, 180)
PINK_LIGHT = (250, 200, 230)
PURPLE = (80, 20, 80)
RED = (220, 40, 80)
WHITE = (250, 250, 250)
BLACK = (10, 10, 25)
GREY = (40, 40, 60)
DARK_GREY = (25, 25, 30)
GREEN_ZOMBIE = (130, 200, 160)
YELLOW = (250, 230, 120)
ORANGE = (255, 150, 50)
BLUE_SKY = (100, 150, 255)
WOOD_DARK = (80, 50, 20)
WOOD_LIGHT = (140, 90, 40)

# ------------------------- SOUND -------------------------
def load_sound(name):
    if not sound_enabled:
        return None
    path = os.path.join("assets", "sfx", name)
    if not os.path.exists(path):
        return None
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return None

def play_sound(snd):
    if snd and sound_enabled:
        snd.play()

def start_music():
    if not sound_enabled:
        return
    path = os.path.join("assets", "sfx", "mario_theme.wav")
    if os.path.exists(path):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

SND_JUMP = load_sound("jump.wav")
SND_COIN = load_sound("coin.wav")
SND_PIPE = load_sound("pipe.wav")
SND_STAGE_CLEAR = load_sound("stage_clear.wav")
SND_POWERUP = load_sound("powerup.wav")
SND_KISS = load_sound("kiss.wav")
SND_LIGHTNING = load_sound("lightning.wav")

# ------------------------- UI -------------------------
class Button:
    def __init__(self, rect, text, base_color=PINK, hover_color=PINK_LIGHT):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.base_color = base_color
        self.hover_color = hover_color

    def draw(self, surf):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        pygame.draw.rect(surf, color, self.rect, border_radius=12)
        pygame.draw.rect(surf, WHITE, self.rect, 3, border_radius=12)
        txt = FONT_MED.render(self.text, True, WHITE)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

# ------------------------- MARIO GIRL -------------------------
class MarioGirl:
    def __init__(self, x=WIDTH//2, y=HEIGHT-150):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.jump_power = -14
        self.gravity = 0.8
        self.on_ground = False
        self.facing_right = True
        self.walk_frame = 0
        self.rect = pygame.Rect(self.x, self.y, 32, 48)

    def handle_keys(self, keys):
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -self.speed
            self.facing_right = False
            self.walk_frame += 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.speed
            self.facing_right = True
            self.walk_frame += 1
        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False
            play_sound(SND_JUMP)

        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        if self.y >= HEIGHT - 100:
            self.y = HEIGHT - 100
            self.vy = 0
            self.on_ground = True
        self.x = max(0, min(self.x, WIDTH - 32))
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf):
        x, y = int(self.x), int(self.y)
        pygame.draw.ellipse(surf, PINK_DARK, (x+2, y-2, 28, 14))
        pygame.draw.circle(surf, PINK_LIGHT, (x+16, y+4), 10)
        pygame.draw.rect(surf, PINK_DARK, (x+4, y, 24, 10), 0, 6)
        pygame.draw.ellipse(surf, MARIO_SKIN, (x+6, y+10, 20, 16))
        eye_offset = 1 if not self.facing_right else -1
        pygame.draw.circle(surf, BLACK, (x+11 + eye_offset, y+16), 2)
        pygame.draw.circle(surf, BLACK, (x+21 + eye_offset, y+16), 2)
        pygame.draw.circle(surf, MARIO_RED, (x+16, y+19), 2)
        pygame.draw.rect(surf, MARIO_BLUE, (x+8, y+26, 16, 18), 0, 4)
        pygame.draw.circle(surf, YELLOW, (x+12, y+28), 2)
        pygame.draw.circle(surf, YELLOW, (x+20, y+28), 2)
        pygame.draw.polygon(surf, PINK, [(x+8, y+35), (x+24, y+35), (x+26, y+44), (x+6, y+44)])
        arm_y = 2 if self.walk_frame % 20 < 10 else 0
        pygame.draw.rect(surf, MARIO_SKIN, (x+2, y+28 + arm_y, 6, 12), 0, 2)
        pygame.draw.rect(surf, MARIO_SKIN, (x+24, y+28 - arm_y, 6, 12), 0, 2)
        leg_offset = 3 if self.walk_frame % 20 < 10 else -3
        pygame.draw.rect(surf, YELLOW, (x+9 + leg_offset, y+44, 6, 4), 0, 2)
        pygame.draw.rect(surf, YELLOW, (x+17 - leg_offset, y+44, 6, 4), 0, 2)

# ------------------------- BODY PARTS -------------------------
PART_NAMES = ["Legs", "Hands", "Torso", "Head", "Brain", "Heart"]

class BodyPart:
    def __init__(self, name, pos):
        self.name = name
        self.rect = pygame.Rect(pos[0], pos[1], 50, 45)
        self.collected = False
        self.float_offset = 0
        self.sparkle_timer = 0

    def update(self):
        self.float_offset = math.sin(pygame.time.get_ticks() / 200) * 8
        self.sparkle_timer += 1

    def draw(self, surf):
        if self.collected:
            return
        x, y = self.rect.x, self.rect.y + self.float_offset

        # Glow
        glow_radius = 30 + math.sin(self.sparkle_timer / 10) * 3
        for i in range(3):
            alpha = 100 - i * 30
            glow_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 215, 0, alpha), (40, 40), int(glow_radius - i*5))
            surf.blit(glow_surf, (x-15, y-15))

        # Draw part based on type
        if self.name == "Heart":
            draw_heart(surf, (x + 25, y + 20), RED, 20)
        elif self.name == "Legs":
            pygame.draw.rect(surf, MARIO_SKIN, (x+12, y+10, 12, 25), 0, 4)
            pygame.draw.rect(surf, MARIO_SKIN, (x+26, y+10, 12, 25), 0, 4)
        elif self.name == "Hands":
            pygame.draw.circle(surf, MARIO_SKIN, (x+15, y+20), 12)
            pygame.draw.circle(surf, MARIO_SKIN, (x+35, y+20), 12)
        elif self.name == "Torso":
            pygame.draw.rect(surf, MARIO_SKIN, (x+10, y+5, 30, 35), 0, 8)
        elif self.name == "Head":
            pygame.draw.circle(surf, MARIO_SKIN, (x+25, y+22), 18)
        elif self.name == "Brain":
            pygame.draw.ellipse(surf, PINK, (x+10, y+10, 30, 25))

        pygame.draw.rect(surf, YELLOW, (self.rect.x-2, self.rect.y + self.float_offset-2, 54, 49), 3, 8)
        name_bg = FONT_TINY.render(self.name, True, WHITE)
        surf.blit(name_bg, (x+5, y+40))

# ------------------------- ASSEMBLY -------------------------
ASSEMBLY_ORDER = ["Legs", "Torso", "Hands", "Head", "Brain", "Heart"]

class AssemblySlot:
    def __init__(self, name, center):
        self.name = name
        self.center = center
        self.filled = False
        self.pulse = 0

    def update(self):
        self.pulse += 0.1

    def draw(self, surf):
        scale = 1 + math.sin(self.pulse) * 0.05 if not self.filled else 1
        w, h = int(80 * scale), int(60 * scale)
        rect = pygame.Rect(0, 0, w, h)
        rect.center = self.center

        if self.filled:
            x, y = rect.centerx - 25, rect.centery - 22
            if self.name == "Legs":
                pygame.draw.rect(surf, GREEN_ZOMBIE, (x+12, y+10, 12, 30), 0, 4)
                pygame.draw.rect(surf, GREEN_ZOMBIE, (x+26, y+10, 12, 30), 0, 4)
            elif self.name == "Torso":
                pygame.draw.rect(surf, GREEN_ZOMBIE, (x+10, y+5, 30, 40), 0, 8)
            elif self.name == "Hands":
                pygame.draw.circle(surf, GREEN_ZOMBIE, (x+15, y+22), 10)
                pygame.draw.circle(surf, GREEN_ZOMBIE, (x+35, y+22), 10)
            elif self.name == "Head":
                pygame.draw.circle(surf, GREEN_ZOMBIE, (x+25, y+22), 18)
            elif self.name == "Brain":
                pygame.draw.ellipse(surf, PINK, (x+10, y+10, 30, 22))
            elif self.name == "Heart":
                draw_heart(surf, (x+25, y+22), RED, 16)
        else:
            pygame.draw.rect(surf, GREY, rect, 0, 12)
            pygame.draw.rect(surf, PINK_LIGHT, rect, 4, 12)
            label = FONT_SMALL.render(self.name, True, WHITE)
            surf.blit(label, label.get_rect(center=self.center))

# ------------------------- ROOM SYSTEM -------------------------
ROOMS = ["Bedroom", "Living Room", "Kitchen", "Lab"]

def draw_heart(surf, pos, color, size=14):
    x, y = pos
    pygame.draw.circle(surf, color, (x - size//4, y), size//4)
    pygame.draw.circle(surf, color, (x + size//4, y), size//4)
    pygame.draw.polygon(surf, color, [(x - size//2, y), (x + size//2, y), (x, y + size//2)])

def draw_room_background(room_name):
    """Draw room backgrounds"""
    SCREEN.fill((50, 40, 30))
    if room_name != "Lab":
        for y in range(0, HEIGHT - 100, 2):
            shade = int(100 + (y / (HEIGHT - 100)) * 100)
            color = (shade, shade + 30, 255)
            pygame.draw.line(SCREEN, color, (0, y), (WIDTH, y))
    else:
        SCREEN.fill(DARK_GREY)
        pygame.draw.rect(SCREEN, PURPLE, (0, 0, WIDTH, HEIGHT - 100))

    # Floor
    for x in range(0, WIDTH, 50):
        pygame.draw.rect(SCREEN, WOOD_DARK, (x, HEIGHT-100, 48, 98))
        pygame.draw.rect(SCREEN, WOOD_LIGHT, (x+3, HEIGHT-97, 42, 92), 0, 3)

def draw_door(x, y):
    """Draw Mario pipe door"""
    pygame.draw.rect(SCREEN, MARIO_GREEN, (x-28, y-75, 56, 95), 0, 12)
    pygame.draw.rect(SCREEN, (30, 160, 40), (x-25, y-72, 50, 89), 0, 10)
    pygame.draw.ellipse(SCREEN, MARIO_GREEN, (x-32, y-82, 64, 24))
    pygame.draw.ellipse(SCREEN, BLACK, (x-20, y-55, 40, 40))

async def room_transition_effect(from_room, to_room):
    """WEB SAFE: Pipe warp transition"""
    play_sound(SND_PIPE)
    for i in range(40):
        SCREEN.fill(BLACK)
        for j in range(12):
            angle = (i * 15 + j * 30) % 360
            rad = math.radians(angle)
            radius = 150 - i * 3
            x = WIDTH//2 + math.cos(rad) * radius
            y = HEIGHT//2 + math.sin(rad) * radius
            color = MARIO_GREEN if j % 2 == 0 else PINK
            size = int(20 - i * 0.4)
            pygame.draw.circle(SCREEN, color, (int(x), int(y)), max(3, size))

        text = FONT_BIG.render(to_room, True, WHITE)
        SCREEN.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
        pygame.display.flip()
        CLOCK.tick(40)
        await asyncio.sleep(0)  # WEB SAFE
    await asyncio.sleep(0.4)  # WEB SAFE - replaces pygame.time.delay

# ------------------------- STATES -------------------------
STATE_TITLE = "TITLE"
STATE_STAGE1 = "STAGE1"
STATE_STAGE2 = "STAGE2"
STATE_STAGE3 = "STAGE3"
STATE_ENDING = "ENDING"

# ------------------------- SCENES -------------------------
async def title_scene():
    """WEB SAFE: Title screen"""
    start_button = Button((WIDTH//2 - 140, HEIGHT//2 + 80, 280, 80), "ðŸŽ® Start Game")
    particles = []
    for _ in range(40):
        particles.append({
            'x': random.randint(0, WIDTH),
            'y': random.randint(0, HEIGHT),
            'speed': random.uniform(0.3, 1.5),
            'size': random.randint(4, 10)
        })

    running = True
    while running:
        await asyncio.sleep(0)  # WEB SAFE
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.is_clicked(event):
                play_sound(SND_COIN)
                return STATE_STAGE1

        # Gradient
        for y in range(0, HEIGHT, 3):
            shade = int(140 + (y / HEIGHT) * 60)
            pygame.draw.line(SCREEN, (shade, 20, 90), (0, y), (WIDTH, y))

        # Floating hearts
        for p in particles:
            p['y'] += p['speed']
            if p['y'] > HEIGHT:
                p['y'] = 0
                p['x'] = random.randint(0, WIDTH)
            draw_heart(SCREEN, (p['x'], int(p['y'])), PINK_LIGHT, p['size'])

        # Title
        title_text = "Will You Be Frankenstien?"
        title = FONT_BIG.render(title_text, True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 120))
        sub = FONT_MED.render("ðŸŽ® Mario x Valentine Horror ðŸ’•", True, MARIO_RED)
        SCREEN.blit(sub, sub.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
        controls = FONT_SMALL.render("Arrow Keys/WASD: Move | SPACE/UP: Jump", True, WHITE)
        SCREEN.blit(controls, controls.get_rect(center=(WIDTH//2, HEIGHT - 60)))
        start_button.draw(SCREEN)
        pygame.display.flip()

async def stage1_scene():
    """WEB SAFE: Collect body parts"""
    girl = MarioGirl()
    current_room = "Bedroom"

    part_positions = {
        "Bedroom": [(150, HEIGHT-160), (250, HEIGHT-200)],
        "Living Room": [(500, HEIGHT-160), (650, HEIGHT-180)],
        "Kitchen": [(350, HEIGHT-140), (550, HEIGHT-170)],
    }

    all_parts = []
    for room, positions in part_positions.items():
        for i, pos in enumerate(positions):
            part_idx = list(part_positions.keys()).index(room) * 2 + i
            if part_idx < len(PART_NAMES):
                part = BodyPart(PART_NAMES[part_idx], pos)
                part.room = room
                all_parts.append(part)

    collected_count = 0
    total_parts = len(all_parts)

    doors = {
        "Bedroom": (WIDTH - 60, HEIGHT - 160),
        "Living Room": (60, HEIGHT - 160),
        "Kitchen": (WIDTH - 60, HEIGHT - 160),
    }

    running = True
    while running:
        await asyncio.sleep(0)  # WEB SAFE
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        girl.handle_keys(keys)

        # Collect parts
        for part in all_parts:
            if part.room == current_room and not part.collected:
                part.update()
                if girl.rect.colliderect(part.rect):
                    part.collected = True
                    collected_count += 1
                    play_sound(SND_COIN)

        # Door collision
        if current_room in doors:
            door_x, door_y = doors[current_room]
            door_rect = pygame.Rect(door_x - 35, door_y - 80, 70, 100)
            if girl.rect.colliderect(door_rect):
                room_index = ROOMS.index(current_room)
                next_room = ROOMS[(room_index + 1) % len(ROOMS)]
                if next_room == "Lab" and collected_count < total_parts:
                    next_room = ROOMS[0]
                await room_transition_effect(current_room, next_room)
                current_room = next_room
                girl.x = WIDTH - 120 if current_room == "Living Room" else 100
                girl.y = HEIGHT - 150

        # Stage complete
        if current_room == "Lab" and collected_count == total_parts:
            play_sound(SND_STAGE_CLEAR)
            await asyncio.sleep(1.0)  # WEB SAFE
            return STATE_STAGE2

        # Draw
        draw_room_background(current_room)
        if current_room in doors:
            draw_door(*doors[current_room])
        for part in all_parts:
            if part.room == current_room:
                part.draw(SCREEN)
        girl.draw(SCREEN)

        # HUD
        hud_text = f"ðŸ“ {current_room} | ðŸ§© Parts: {collected_count}/{total_parts}"
        hud_surf = FONT_SMALL.render(hud_text, True, WHITE)
        SCREEN.blit(hud_surf, (30, 25))

        if collected_count == total_parts:
            msg = FONT_MED.render("âœ¨ All parts found! Enter the pipe to Lab! âœ¨", True, YELLOW)
            SCREEN.blit(msg, msg.get_rect(center=(WIDTH//2, 80)))

        pygame.display.flip()

async def stage2_scene():
    """WEB SAFE: Assembly stage"""
    slots = []
    positions = {
        "Legs": (WIDTH//2, HEIGHT//2 + 80),
        "Torso": (WIDTH//2, HEIGHT//2 + 20),
        "Hands": (WIDTH//2, HEIGHT//2 - 40),
        "Head": (WIDTH//2, HEIGHT//2 - 100),
        "Brain": (WIDTH//2 + 100, HEIGHT//2 - 100),
        "Heart": (WIDTH//2 - 100, HEIGHT//2 + 20)
    }

    for name in ASSEMBLY_ORDER:
        slots.append(AssemblySlot(name, positions[name]))

    next_index = 0
    running = True

    while running:
        await asyncio.sleep(0)  # WEB SAFE
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if next_index < len(slots):
                    slots[next_index].filled = True
                    next_index += 1
                    play_sound(SND_POWERUP)

        draw_room_background("Lab")
        title = FONT_BIG.render("âš¡ Stage 2: Assembly âš¡", True, YELLOW)
        SCREEN.blit(title, title.get_rect(center=(WIDTH//2, 60)))

        for s in slots:
            s.update()
            s.draw(SCREEN)

        if next_index < len(ASSEMBLY_ORDER):
            tip = f"ðŸ–±ï¸ Click to place: {ASSEMBLY_ORDER[next_index]}"
            tip_surf = FONT_SMALL.render(tip, True, WHITE)
            SCREEN.blit(tip_surf, (35, HEIGHT - 45))

        if next_index == len(slots):
            done_msg = FONT_BIG.render("ðŸ’€ Ready for Life! ðŸ’€", True, GREEN_ZOMBIE)
            SCREEN.blit(done_msg, done_msg.get_rect(center=(WIDTH//2, HEIGHT - 60)))
            pygame.display.flip()
            play_sound(SND_STAGE_CLEAR)
            await asyncio.sleep(2.5)  # WEB SAFE
            return STATE_STAGE3

        pygame.display.flip()

async def stage3_scene():
    """WEB SAFE: Choose awakening method"""
    lightning_btn = Button((WIDTH//2 - 300, HEIGHT//2 + 80, 240, 90), "âš¡ Lightning", YELLOW, ORANGE)
    kiss_btn = Button((WIDTH//2 + 60, HEIGHT//2 + 80, 240, 90), "ðŸ’‹ Kiss", PINK, PINK_LIGHT)
    pulse = 0
    choice = None
    running = True

    while running:
        await asyncio.sleep(0)  # WEB SAFE
        CLOCK.tick(60)
        pulse += 0.08

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if lightning_btn.is_clicked(event):
                play_sound(SND_LIGHTNING)
                choice = "LIGHTNING"
                running = False
            if kiss_btn.is_clicked(event):
                play_sound(SND_KISS)
                choice = "KISS"
                running = False

        SCREEN.fill(BLACK)
        title = FONT_BIG.render("âš¡ Stage 3: Awakening ðŸ’•", True, WHITE)
        SCREEN.blit(title, title.get_rect(center=(WIDTH//2, 70)))
        q = FONT_MED.render("Choose your method...", True, PINK_LIGHT)
        SCREEN.blit(q, q.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))
        lightning_btn.draw(SCREEN)
        kiss_btn.draw(SCREEN)
        pygame.display.flip()

    return STATE_ENDING, choice

async def ending_scene(choice):
    """WEB SAFE: Ending cutscene"""
    timer = 0
    duration = 7000
    hugging = choice == "KISS"
    particles = []

    while timer < duration:
        await asyncio.sleep(0)  # WEB SAFE
        dt = CLOCK.tick(60)
        timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill(BLACK)

        if hugging:
            if random.random() < 0.4:
                particles.append({
                    'x': random.randint(0, WIDTH),
                    'y': HEIGHT,
                    'vy': -random.uniform(2, 5),
                    'vx': random.uniform(-1, 1),
                    'size': random.randint(10, 20)
                })
            for p in particles:
                p['y'] += p['vy']
                p['x'] += p['vx']
                draw_heart(SCREEN, (int(p['x']), int(p['y'])), PINK, p['size'])
            particles = [p for p in particles if p['y'] > -50]

            msg1 = FONT_BIG.render("ðŸ’‹ True Love's Kiss! ðŸ§Ÿ", True, PINK_LIGHT)
            SCREEN.blit(msg1, msg1.get_rect(center=(WIDTH//2, 90)))
            msg2 = FONT_BIG.render("ðŸ’• Happy Creepy Valentine! ðŸ’•", True, MARIO_RED)
            SCREEN.blit(msg2, msg2.get_rect(center=(WIDTH//2, HEIGHT - 80)))
        else:
            msg1 = FONT_BIG.render("âš¡ Lightning Strike! âš¡", True, YELLOW)
            SCREEN.blit(msg1, msg1.get_rect(center=(WIDTH//2, 90)))
            msg2 = FONT_MED.render("The spark fades... ðŸ’”", True, WHITE)
            SCREEN.blit(msg2, msg2.get_rect(center=(WIDTH//2, 150)))

        pygame.display.flip()

    return await ending_menu()

async def ending_menu():
    """WEB SAFE: Play again menu"""
    play_again_btn = Button((WIDTH//2 - 310, HEIGHT//2 + 50, 280, 90), "ðŸ”„ Play Again")
    quit_btn = Button((WIDTH//2 + 30, HEIGHT//2 + 50, 280, 90), "ðŸšª Quit", GREY, (90, 90, 100))

    while True:
        await asyncio.sleep(0)  # WEB SAFE
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if play_again_btn.is_clicked(event):
                play_sound(SND_COIN)
                return STATE_STAGE1
            if quit_btn.is_clicked(event):
                pygame.quit()
                sys.exit()

        SCREEN.fill(DARK_GREY)
        msg = FONT_BIG.render("Experiment Complete", True, GREEN_ZOMBIE)
        SCREEN.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2 - 100)))
        play_again_btn.draw(SCREEN)
        quit_btn.draw(SCREEN)
        pygame.display.flip()

# ------------------------- MAIN -------------------------
async def main():
    """WEB SAFE: Main game loop with click-to-start"""
    # BROWSER AUDIO POLICY: Click-to-start screen
    SCREEN.fill(BLACK)
    title = FONT_BIG.render("Click to Start", True, WHITE)
    SCREEN.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
    subtitle = FONT_SMALL.render("(Click anywhere or press any key)", True, PINK)
    SCREEN.blit(subtitle, subtitle.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))
    pygame.display.flip()

    # Wait for user interaction
    waiting = True
    while waiting:
        await asyncio.sleep(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting = False
                break

    start_music()
    state = STATE_TITLE
    choice = None

    while True:
        if state == STATE_TITLE:
            state = await title_scene()
        elif state == STATE_STAGE1:
            state = await stage1_scene()
        elif state == STATE_STAGE2:
            state = await stage2_scene()
        elif state == STATE_STAGE3:
            state, choice = await stage3_scene()
        elif state == STATE_ENDING:
            state = await ending_scene(choice)

        await asyncio.sleep(0)  # WEB SAFE

if __name__ == "__main__":
    asyncio.run(main())
