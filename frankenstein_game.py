#!/usr/bin/env python3
"""
Will You Be Frankenstien? - Super Mario Style Edition
Enhanced graphics with detailed body parts and room decorations.
Includes all sound effects!
"""

import pygame
import sys
import os
import math
import random

# ------------------------- INIT -------------------------
pygame.init()

# Safe audio init for Codespaces
sound_enabled = True
try:
    pygame.mixer.init()
except pygame.error:
    sound_enabled = False
    print("⚠️  Audio disabled: no device available")

WIDTH, HEIGHT = 1000, 650
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Will You Be Frankenstien? 🎮💕")
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

        # Hat
        pygame.draw.ellipse(surf, PINK_DARK, (x+2, y-2, 28, 14))
        pygame.draw.circle(surf, PINK_LIGHT, (x+16, y+4), 10)
        pygame.draw.rect(surf, PINK_DARK, (x+4, y, 24, 10), 0, 6)

        # Face
        pygame.draw.ellipse(surf, MARIO_SKIN, (x+6, y+10, 20, 16))
        eye_offset = 1 if not self.facing_right else -1
        pygame.draw.circle(surf, BLACK, (x+11 + eye_offset, y+16), 2)
        pygame.draw.circle(surf, BLACK, (x+21 + eye_offset, y+16), 2)
        pygame.draw.circle(surf, MARIO_RED, (x+16, y+19), 2)
        pygame.draw.ellipse(surf, BLACK, (x+10, y+21, 6, 3))
        pygame.draw.ellipse(surf, BLACK, (x+16, y+21, 6, 3))

        # Body
        pygame.draw.rect(surf, MARIO_BLUE, (x+8, y+26, 16, 18), 0, 4)
        pygame.draw.rect(surf, MARIO_BLUE, (x+11, y+26, 3, 8))
        pygame.draw.rect(surf, MARIO_BLUE, (x+18, y+26, 3, 8))
        pygame.draw.circle(surf, YELLOW, (x+12, y+28), 2)
        pygame.draw.circle(surf, YELLOW, (x+20, y+28), 2)

        # Dress
        pygame.draw.polygon(surf, PINK, [(x+8, y+35), (x+24, y+35), (x+26, y+44), (x+6, y+44)])

        # Arms
        arm_y = 2 if self.walk_frame % 20 < 10 else 0
        pygame.draw.rect(surf, MARIO_SKIN, (x+2, y+28 + arm_y, 6, 12), 0, 2)
        pygame.draw.circle(surf, MARIO_SKIN, (x+5, y+28 + arm_y), 3)
        pygame.draw.rect(surf, MARIO_SKIN, (x+24, y+28 - arm_y, 6, 12), 0, 2)
        pygame.draw.circle(surf, MARIO_SKIN, (x+27, y+28 - arm_y), 3)

        # Boots
        leg_offset = 3 if self.walk_frame % 20 < 10 else -3
        pygame.draw.rect(surf, YELLOW, (x+9 + leg_offset, y+44, 6, 4), 0, 2)
        pygame.draw.rect(surf, YELLOW, (x+17 - leg_offset, y+44, 6, 4), 0, 2)

# ------------------------- ENHANCED BODY PARTS -------------------------
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

        # Enhanced coin-like background with glow
        glow_radius = 30 + math.sin(self.sparkle_timer / 10) * 3
        for i in range(3):
            alpha = 100 - i * 30
            glow_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 215, 0, alpha), (40, 40), int(glow_radius - i*5))
            surf.blit(glow_surf, (x-15, y-15))

        # Main body part with detailed graphics
        if self.name == "Heart":
            # Detailed heart
            draw_heart(surf, (x + 25, y + 20), RED, 20)
            pygame.draw.circle(surf, PINK_LIGHT, (x + 25, y + 20), 8)
        elif self.name == "Legs":
            # Two legs
            pygame.draw.rect(surf, MARIO_SKIN, (x+12, y+10, 12, 25), 0, 4)
            pygame.draw.rect(surf, MARIO_SKIN, (x+26, y+10, 12, 25), 0, 4)
            pygame.draw.rect(surf, MARIO_BROWN, (x+10, y+32, 14, 8), 0, 3)
            pygame.draw.rect(surf, MARIO_BROWN, (x+24, y+32, 14, 8), 0, 3)
        elif self.name == "Hands":
            # Two hands
            pygame.draw.circle(surf, MARIO_SKIN, (x+15, y+20), 12)
            pygame.draw.circle(surf, MARIO_SKIN, (x+35, y+20), 12)
            for i in range(5):
                pygame.draw.circle(surf, MARIO_SKIN, (x+10 + i*3, y+25), 3)
                pygame.draw.circle(surf, MARIO_SKIN, (x+30 + i*3, y+25), 3)
        elif self.name == "Torso":
            # Ribcage
            pygame.draw.rect(surf, MARIO_SKIN, (x+10, y+5, 30, 35), 0, 8)
            for i in range(5):
                pygame.draw.line(surf, GREY, (x+15, y+10 + i*6), (x+35, y+10 + i*6), 2)
        elif self.name == "Head":
            # Skull/head
            pygame.draw.circle(surf, MARIO_SKIN, (x+25, y+22), 18)
            pygame.draw.ellipse(surf, BLACK, (x+18, y+18, 6, 8))
            pygame.draw.ellipse(surf, BLACK, (x+28, y+18, 6, 8))
            pygame.draw.rect(surf, BLACK, (x+22, y+30, 6, 8), 0, 2)
        elif self.name == "Brain":
            # Brain with wrinkles
            pygame.draw.ellipse(surf, PINK, (x+10, y+10, 30, 25))
            for i in range(4):
                pygame.draw.arc(surf, PINK_DARK, (x+12 + i*6, y+12, 12, 10), 0, 3.14, 2)
                pygame.draw.arc(surf, PINK_DARK, (x+15 + i*6, y+18, 10, 8), 0, 3.14, 2)

        # Border and label
        pygame.draw.rect(surf, YELLOW, (self.rect.x-2, self.rect.y + self.float_offset-2, 54, 49), 3, 8)

        # Name tag
        name_bg = FONT_TINY.render(self.name, True, WHITE)
        name_rect = name_bg.get_rect(center=(x + 25, y + 52))
        bg_rect = name_rect.inflate(10, 4)
        pygame.draw.rect(surf, BLACK, bg_rect, 0, 4)
        pygame.draw.rect(surf, YELLOW, bg_rect, 2, 4)
        surf.blit(name_bg, name_rect)

# ------------------------- ENHANCED ASSEMBLY -------------------------
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
            # Draw actual body part
            x, y = rect.centerx - 25, rect.centery - 22
            if self.name == "Legs":
                pygame.draw.rect(surf, GREEN_ZOMBIE, (x+12, y+10, 12, 30), 0, 4)
                pygame.draw.rect(surf, GREEN_ZOMBIE, (x+26, y+10, 12, 30), 0, 4)
            elif self.name == "Torso":
                pygame.draw.rect(surf, GREEN_ZOMBIE, (x+10, y+5, 30, 40), 0, 8)
                for i in range(5):
                    pygame.draw.line(surf, DARK_GREY, (x+15, y+10 + i*7), (x+35, y+10 + i*7), 2)
            elif self.name == "Hands":
                pygame.draw.circle(surf, GREEN_ZOMBIE, (x+15, y+22), 10)
                pygame.draw.circle(surf, GREEN_ZOMBIE, (x+35, y+22), 10)
            elif self.name == "Head":
                pygame.draw.circle(surf, GREEN_ZOMBIE, (x+25, y+22), 18)
                pygame.draw.circle(surf, BLACK, (x+18, y+20), 4)
                pygame.draw.circle(surf, BLACK, (x+32, y+20), 4)
                pygame.draw.line(surf, BLACK, (x+15, y+10), (x+35, y+12), 3)
            elif self.name == "Brain":
                pygame.draw.ellipse(surf, PINK, (x+10, y+10, 30, 22))
            elif self.name == "Heart":
                draw_heart(surf, (x+25, y+22), RED, 16)
        else:
            # Empty slot
            pygame.draw.rect(surf, GREY, rect, 0, 12)
            pygame.draw.rect(surf, DARK_GREY, rect.inflate(-6, -6), 0, 10)

        pygame.draw.rect(surf, GREEN_ZOMBIE if self.filled else PINK_LIGHT, rect, 4, 12)

        # Label
        if not self.filled:
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
    """Enhanced room graphics with more details"""
    SCREEN.fill((50, 40, 30))

    # Sky/wall with gradient
    if room_name != "Lab":
        for y in range(0, HEIGHT - 100, 2):
            shade = int(100 + (y / (HEIGHT - 100)) * 100)
            color = (shade, shade + 30, 255)
            pygame.draw.line(SCREEN, color, (0, y), (WIDTH, y))
    else:
        SCREEN.fill(DARK_GREY)
        pygame.draw.rect(SCREEN, PURPLE, (0, 0, WIDTH, HEIGHT - 100))

    if room_name == "Bedroom":
        # Wallpaper pattern
        for i in range(15):
            for j in range(8):
                x, y = i * 70, j * 70
                draw_heart(SCREEN, (x, y), PINK_LIGHT, 6)

        # Large bed with details
        pygame.draw.rect(SCREEN, WOOD_DARK, (50, HEIGHT-200, 250, 120), 0, 10)
        pygame.draw.rect(SCREEN, PINK_DARK, (50, HEIGHT-210, 250, 40), 0, 15)
        pygame.draw.rect(SCREEN, PINK_LIGHT, (60, HEIGHT-205, 230, 30), 0, 10)
        # Pillows
        pygame.draw.ellipse(SCREEN, WHITE, (70, HEIGHT-195, 70, 30))
        pygame.draw.ellipse(SCREEN, WHITE, (200, HEIGHT-195, 70, 30))
        # Blanket folds
        for i in range(3):
            pygame.draw.line(SCREEN, PINK, (60, HEIGHT-170 + i*20), (280, HEIGHT-170 + i*20), 3)

        # Nightstand & lamp
        pygame.draw.rect(SCREEN, WOOD_LIGHT, (320, HEIGHT-150, 60, 70), 0, 6)
        pygame.draw.rect(SCREEN, WOOD_DARK, (330, HEIGHT-145, 40, 10), 0, 3)
        pygame.draw.rect(SCREEN, MARIO_BROWN, (345, HEIGHT-180, 10, 30))
        pygame.draw.polygon(SCREEN, YELLOW, [(330, HEIGHT-180), (360, HEIGHT-180), (355, HEIGHT-200), (335, HEIGHT-200)])
        pygame.draw.circle(SCREEN, ORANGE, (345, HEIGHT-205), 10)

        # Window with curtains
        pygame.draw.rect(SCREEN, BLUE_SKY, (WIDTH-200, 50, 120, 150), 0, 8)
        pygame.draw.rect(SCREEN, WOOD_DARK, (WIDTH-200, 50, 120, 150), 5, 8)
        pygame.draw.polygon(SCREEN, PINK, [(WIDTH-200, 50), (WIDTH-180, 50), (WIDTH-180, 200)])
        pygame.draw.polygon(SCREEN, PINK, [(WIDTH-80, 50), (WIDTH-100, 50), (WIDTH-100, 200)])

    elif room_name == "Living Room":
        # Wooden floor pattern
        for i in range(0, WIDTH, 60):
            for j in range(HEIGHT-100, HEIGHT, 20):
                shade = (60, 45, 30) if (i + j) % 40 == 0 else (70, 55, 40)
                pygame.draw.rect(SCREEN, shade, (i, j, 58, 18))

        # Large sofa with cushions
        pygame.draw.rect(SCREEN, WOOD_DARK, (60, HEIGHT-150, 280, 90), 0, 15)
        pygame.draw.rect(SCREEN, MARIO_RED, (70, HEIGHT-145, 260, 70), 0, 12)
        # Armrests
        pygame.draw.rect(SCREEN, MARIO_RED, (60, HEIGHT-145, 25, 70), 0, 8)
        pygame.draw.rect(SCREEN, MARIO_RED, (315, HEIGHT-145, 25, 70), 0, 8)
        # Cushions with details
        for i in range(4):
            cx = 100 + i * 60
            pygame.draw.circle(SCREEN, PINK, (cx, HEIGHT-120), 22)
            pygame.draw.circle(SCREEN, PINK_LIGHT, (cx, HEIGHT-120), 18)

        # Coffee table
        pygame.draw.ellipse(SCREEN, WOOD_LIGHT, (100, HEIGHT-90, 180, 40))
        pygame.draw.rect(SCREEN, WOOD_DARK, (160, HEIGHT-50, 60, 5))

        # Large TV with screen
        pygame.draw.rect(SCREEN, BLACK, (550, HEIGHT-200, 180, 130), 0, 12)
        pygame.draw.rect(SCREEN, GREY, (560, HEIGHT-190, 160, 105), 0, 8)
        # Screen content (static)
        for i in range(20):
            color = random.choice([BLUE_SKY, GREY, WHITE])
            pygame.draw.rect(SCREEN, color, (565 + random.randint(0, 140), HEIGHT-185 + random.randint(0, 85), 8, 8))
        pygame.draw.rect(SCREEN, DARK_GREY, (620, HEIGHT-85, 40, 15), 0, 4)

        # Carpet with pattern
        pygame.draw.ellipse(SCREEN, MARIO_RED, (80, HEIGHT-75, 250, 60))
        for i in range(5):
            pygame.draw.circle(SCREEN, PINK, (120 + i*40, HEIGHT-50), 8)

    elif room_name == "Kitchen":
        # Checkered floor
        for x in range(0, WIDTH, 50):
            for y in range(HEIGHT-100, HEIGHT, 50):
                color = WHITE if ((x + y) // 50) % 2 == 0 else (220, 220, 220)
                pygame.draw.rect(SCREEN, color, (x, y, 48, 48))
                pygame.draw.rect(SCREEN, GREY, (x, y, 48, 48), 1)

        # Large fridge with details
        pygame.draw.rect(SCREEN, WHITE, (40, HEIGHT-270, 110, 190), 0, 12)
        pygame.draw.rect(SCREEN, (240, 240, 250), (50, HEIGHT-260, 90, 80), 0, 8)
        pygame.draw.rect(SCREEN, (240, 240, 250), (50, HEIGHT-170, 90, 90), 0, 8)
        pygame.draw.circle(SCREEN, BLACK, (130, HEIGHT-220), 6)
        pygame.draw.circle(SCREEN, BLACK, (130, HEIGHT-125), 6)
        # Magnets
        pygame.draw.circle(SCREEN, MARIO_RED, (70, HEIGHT-240), 5)
        pygame.draw.circle(SCREEN, YELLOW, (90, HEIGHT-190), 5)
        pygame.draw.circle(SCREEN, MARIO_GREEN, (110, HEIGHT-150), 5)

        # Kitchen counter
        pygame.draw.rect(SCREEN, WOOD_LIGHT, (200, HEIGHT-130, 280, 50), 0, 8)
        pygame.draw.rect(SCREEN, WOOD_DARK, (200, HEIGHT-135, 280, 10), 0, 4)

        # Sink
        pygame.draw.ellipse(SCREEN, GREY, (250, HEIGHT-120, 80, 30))
        pygame.draw.ellipse(SCREEN, (200, 200, 210), (255, HEIGHT-118, 70, 25))
        # Faucet
        pygame.draw.rect(SCREEN, GREY, (285, HEIGHT-145, 8, 25))
        pygame.draw.circle(SCREEN, GREY, (289, HEIGHT-145), 6)

        # Stove with burners
        pygame.draw.rect(SCREEN, (50, 50, 60), (350, HEIGHT-120, 100, 40), 0, 8)
        for i in range(2):
            for j in range(2):
                cx, cy = 375 + i*35, HEIGHT-105 + j*20
                pygame.draw.circle(SCREEN, BLACK, (cx, cy), 12)
                pygame.draw.circle(SCREEN, ORANGE, (cx, cy), 9)
                pygame.draw.circle(SCREEN, YELLOW, (cx, cy), 6)

        # Upper cabinets
        for i in range(3):
            cx = 220 + i*80
            pygame.draw.rect(SCREEN, WOOD_DARK, (cx, HEIGHT-280, 70, 60), 0, 6)
            pygame.draw.rect(SCREEN, WOOD_LIGHT, (cx+5, HEIGHT-275, 60, 50), 0, 4)
            pygame.draw.circle(SCREEN, BLACK, (cx+35, HEIGHT-245), 3)

    elif room_name == "Lab":
        # Dark lab with dramatic lighting
        SCREEN.fill((15, 15, 25))

        # Spooky background elements
        for i in range(20):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT - 200)
            pygame.draw.line(SCREEN, (30, 30, 40), (x, y), (x, y + random.randint(50, 150)), 1)

        # Multiple shelving units
        for i in range(4):
            sx = 50 + i * 220
            pygame.draw.rect(SCREEN, (60, 60, 70), (sx, HEIGHT-280, 140, 200), 0, 8)

            # Shelves
            for j in range(4):
                sy = HEIGHT-270 + j * 50
                pygame.draw.rect(SCREEN, (70, 70, 80), (sx+5, sy, 130, 5))

                # Items on shelves
                if j == 0:
                    # Books
                    for k in range(4):
                        bx = sx + 10 + k * 30
                        book_color = random.choice([MARIO_RED, MARIO_BLUE, MARIO_GREEN, PURPLE])
                        pygame.draw.rect(SCREEN, book_color, (bx, sy-40, 20, 35), 0, 2)
                elif j == 1:
                    # Beakers
                    for k in range(3):
                        bx = sx + 20 + k * 40
                        beaker_color = random.choice([GREEN_ZOMBIE, PINK, YELLOW, ORANGE])
                        pygame.draw.rect(SCREEN, beaker_color, (bx, sy-30, 18, 25), 0, 4)
                        pygame.draw.polygon(SCREEN, beaker_color, [(bx, sy-30), (bx+18, sy-30), (bx+14, sy-40), (bx+4, sy-40)])
                elif j == 2:
                    # Skulls
                    for k in range(2):
                        bx = sx + 30 + k * 60
                        pygame.draw.circle(SCREEN, (220, 220, 210), (bx, sy-20), 15)
                        pygame.draw.ellipse(SCREEN, BLACK, (bx-8, sy-24, 6, 8))
                        pygame.draw.ellipse(SCREEN, BLACK, (bx+2, sy-24, 6, 8))
                else:
                    # Jars
                    for k in range(3):
                        bx = sx + 20 + k * 40
                        pygame.draw.rect(SCREEN, (100, 120, 140, 180), (bx, sy-35, 22, 30), 0, 3)
                        pygame.draw.circle(SCREEN, random.choice([PINK, GREEN_ZOMBIE]), (bx+11, sy-20), 5)

        # Operating table/bed (center)
        table_rect = pygame.Rect(WIDTH//2-100, HEIGHT-150, 200, 70)
        pygame.draw.rect(SCREEN, (80, 80, 90), table_rect, 0, 15)
        pygame.draw.rect(SCREEN, (120, 120, 130), table_rect.inflate(-10, -10), 0, 12)
        # Table legs
        pygame.draw.rect(SCREEN, (60, 60, 70), (WIDTH//2-90, HEIGHT-80, 15, 80))
        pygame.draw.rect(SCREEN, (60, 60, 70), (WIDTH//2+75, HEIGHT-80, 15, 80))

        # Mad scientist equipment
        # Tesla coil
        pygame.draw.rect(SCREEN, GREY, (WIDTH-150, HEIGHT-200, 40, 120), 0, 6)
        for i in range(5):
            pygame.draw.circle(SCREEN, (100, 100, 110), (WIDTH-130, HEIGHT-180 + i*25), 22, 3)
        pygame.draw.circle(SCREEN, YELLOW, (WIDTH-130, HEIGHT-210), 15)

        # Lightning effects
        if random.random() < 0.3:
            for i in range(3):
                x1, y1 = WIDTH-130, HEIGHT-210
                x2 = x1 + random.randint(-50, 50)
                y2 = y1 + random.randint(50, 150)
                pygame.draw.line(SCREEN, YELLOW, (x1, y1), (x2, y2), 3)
                pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2, y2), 1)

    # Floor (Mario blocks style)
    for x in range(0, WIDTH, 50):
        pygame.draw.rect(SCREEN, WOOD_DARK, (x, HEIGHT-100, 48, 98))
        pygame.draw.rect(SCREEN, WOOD_LIGHT, (x+3, HEIGHT-97, 42, 92), 0, 3)
        pygame.draw.rect(SCREEN, WOOD_DARK, (x+3, HEIGHT-97, 42, 92), 2, 3)

def draw_door(x, y):
    """Enhanced Mario pipe door"""
    # Shadow
    shadow_surf = pygame.Surface((70, 100), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surf, (0, 0, 0, 80), (0, 70, 70, 30))
    SCREEN.blit(shadow_surf, (x-35, y-35))

    # Pipe body
    pygame.draw.rect(SCREEN, MARIO_GREEN, (x-28, y-75, 56, 95), 0, 12)
    pygame.draw.rect(SCREEN, (30, 160, 40), (x-25, y-72, 50, 89), 0, 10)

    # Pipe rim (top)
    pygame.draw.ellipse(SCREEN, MARIO_GREEN, (x-32, y-82, 64, 24))
    pygame.draw.ellipse(SCREEN, (30, 160, 40), (x-29, y-79, 58, 18))
    pygame.draw.ellipse(SCREEN, (20, 120, 30), (x-26, y-76, 52, 12))

    # Pipe opening (black hole)
    pygame.draw.ellipse(SCREEN, BLACK, (x-20, y-55, 40, 40))
    pygame.draw.ellipse(SCREEN, (20, 20, 20), (x-18, y-53, 36, 36))

    # Shine effect
    pygame.draw.arc(SCREEN, (80, 255, 80), (x-25, y-78, 20, 15), 0, 3.14, 2)

def room_transition_effect(from_room, to_room):
    """Enhanced pipe warp transition"""
    play_sound(SND_PIPE)

    for i in range(40):
        SCREEN.fill(BLACK)

        # Spinning vortex
        for j in range(12):
            angle = (i * 15 + j * 30) % 360
            rad = math.radians(angle)
            radius = 150 - i * 3
            x = WIDTH//2 + math.cos(rad) * radius
            y = HEIGHT//2 + math.sin(rad) * radius
            color = MARIO_GREEN if j % 2 == 0 else PINK
            size = int(20 - i * 0.4)
            pygame.draw.circle(SCREEN, color, (int(x), int(y)), max(3, size))

        # Center text
        alpha = min(255, i * 8)
        text = FONT_BIG.render(to_room, True, WHITE)
        text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
        text_surface.blit(text, (0, 0))
        text_surface.set_alpha(alpha)
        SCREEN.blit(text_surface, text.get_rect(center=(WIDTH//2, HEIGHT//2)))

        pygame.display.flip()
        CLOCK.tick(40)

    pygame.time.delay(400)

# ------------------------- STATES -------------------------
STATE_TITLE = "TITLE"
STATE_STAGE1 = "STAGE1"
STATE_STAGE2 = "STAGE2"
STATE_STAGE3 = "STAGE3"
STATE_ENDING = "ENDING"

# ------------------------- SCENES -------------------------
def title_scene():
    start_button = Button((WIDTH//2 - 140, HEIGHT//2 + 80, 280, 80), "🎮 Start Game")

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
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.is_clicked(event):
                play_sound(SND_COIN)
                return STATE_STAGE1

        # Gradient background
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

        # Title with shadow
        title_text = "Will You Be Frankenstien?"
        for offset in [(4, 4), (2, 2)]:
            shadow = FONT_BIG.render(title_text, True, BLACK)
            SCREEN.blit(shadow, (WIDTH//2 - shadow.get_width()//2 + offset[0], HEIGHT//2 - 120 + offset[1]))

        title = FONT_BIG.render(title_text, True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 120))

        # Subtitle
        sub = FONT_MED.render("🎮 Mario x Valentine Horror 💕", True, MARIO_RED)
        SCREEN.blit(sub, sub.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))

        # Controls
        controls = FONT_SMALL.render("Arrow Keys/WASD: Move  |  SPACE/UP: Jump", True, WHITE)
        SCREEN.blit(controls, controls.get_rect(center=(WIDTH//2, HEIGHT - 60)))

        start_button.draw(SCREEN)
        pygame.display.flip()

def stage1_scene():
    girl = MarioGirl()
    current_room = "Bedroom"

    # Distribute parts across rooms
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

                # Go to lab only if all collected
                if next_room == "Lab" and collected_count < total_parts:
                    next_room = ROOMS[0]

                room_transition_effect(current_room, next_room)
                current_room = next_room
                girl.x = WIDTH - 120 if current_room == "Living Room" else 100
                girl.y = HEIGHT - 150

                # Stage complete
                if current_room == "Lab" and collected_count == total_parts:
                    play_sound(SND_STAGE_CLEAR)
                    pygame.time.delay(1000)
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
        hud_text = f"📍 {current_room}  |  🧩 Parts: {collected_count}/{total_parts}"
        hud_surf = FONT_SMALL.render(hud_text, True, WHITE)
        hud_bg = pygame.Rect(15, 15, hud_surf.get_width() + 30, hud_surf.get_height() + 20)
        pygame.draw.rect(SCREEN, BLACK, hud_bg, 0, 10)
        pygame.draw.rect(SCREEN, PINK, hud_bg, 4, 10)
        SCREEN.blit(hud_surf, (30, 25))

        if collected_count == total_parts:
            msg = FONT_MED.render("✨ All parts found! Enter the pipe to Lab! ✨", True, YELLOW)
            msg_rect = msg.get_rect(center=(WIDTH//2, 80))
            bg = msg_rect.inflate(30, 20)
            pygame.draw.rect(SCREEN, BLACK, bg, 0, 12)
            pygame.draw.rect(SCREEN, MARIO_GREEN, bg, 4, 12)
            SCREEN.blit(msg, msg_rect)

        pygame.display.flip()

def stage2_scene():
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

        # Draw lab
        draw_room_background("Lab")

        # Operating table highlight
        table_glow = pygame.Surface((350, 280), pygame.SRCALPHA)
        pygame.draw.ellipse(table_glow, (100, 255, 100, 30), (0, 0, 350, 280))
        SCREEN.blit(table_glow, (WIDTH//2 - 175, HEIGHT//2 - 140))

        # Title
        title = FONT_BIG.render("⚡ Stage 2: Assembly ⚡", True, YELLOW)
        SCREEN.blit(title, title.get_rect(center=(WIDTH//2, 60)))

        # Update and draw slots
        for s in slots:
            s.update()
            s.draw(SCREEN)

        # Instructions
        if next_index < len(ASSEMBLY_ORDER):
            tip = f"🖱️ Click to place: {ASSEMBLY_ORDER[next_index]}"
            tip_surf = FONT_SMALL.render(tip, True, WHITE)
            tip_bg = pygame.Rect(20, HEIGHT - 60, tip_surf.get_width() + 30, 45)
            pygame.draw.rect(SCREEN, BLACK, tip_bg, 0, 10)
            pygame.draw.rect(SCREEN, MARIO_GREEN, tip_bg, 4, 10)
            SCREEN.blit(tip_surf, (35, HEIGHT - 45))

        if next_index == len(slots):
            done_msg = FONT_BIG.render("💀 Ready for Life! 💀", True, GREEN_ZOMBIE)
            SCREEN.blit(done_msg, done_msg.get_rect(center=(WIDTH//2, HEIGHT - 60)))
            pygame.display.flip()
            play_sound(SND_STAGE_CLEAR)
            pygame.time.delay(2500)
            return STATE_STAGE3

        pygame.display.flip()

def stage3_scene():
    lightning_btn = Button((WIDTH//2 - 300, HEIGHT//2 + 80, 240, 90), "⚡ Lightning", YELLOW, ORANGE)
    kiss_btn = Button((WIDTH//2 + 60, HEIGHT//2 + 80, 240, 90), "💋 Kiss", PINK, PINK_LIGHT)

    pulse = 0
    choice = None
    running = True

    while running:
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

        # Heartbeat line
        for x in range(0, WIDTH, 80):
            y_off = int(math.sin(pulse + x/60) * 12)
            pygame.draw.line(SCREEN, MARIO_RED, (x, 120 + y_off), (x+40, 120 + y_off), 4)

        # Title
        title = FONT_BIG.render("⚡ Stage 3: Awakening 💕", True, WHITE)
        SCREEN.blit(title, title.get_rect(center=(WIDTH//2, 70)))

        # Question
        q = FONT_MED.render("Choose your method...", True, PINK_LIGHT)
        SCREEN.blit(q, q.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))

        lightning_btn.draw(SCREEN)
        kiss_btn.draw(SCREEN)

        # Pulsing Frankenstien body
        scale = 1 + math.sin(pulse * 1.5) * 0.06
        body_w, body_h = int(120 * scale), int(220 * scale)
        body_rect = pygame.Rect(WIDTH//2 - body_w//2, HEIGHT//2 - body_h//2 - 20, body_w, body_h)

        # Glow
        glow_surf = pygame.Surface((body_w + 40, body_h + 40), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surf, (130, 255, 160, 60), (0, 0, body_w + 40, body_h + 40))
        SCREEN.blit(glow_surf, (body_rect.x - 20, body_rect.y - 20))

        # Body
        pygame.draw.rect(SCREEN, GREEN_ZOMBIE, body_rect, 0, 18)
        head_y = body_rect.top - int(40 * scale)
        head_r = int(45 * scale)
        pygame.draw.circle(SCREEN, GREEN_ZOMBIE, (WIDTH//2, head_y), head_r)

        # Face details
        pygame.draw.circle(SCREEN, BLACK, (WIDTH//2 - 15, head_y - 5), 5)
        pygame.draw.circle(SCREEN, BLACK, (WIDTH//2 + 15, head_y - 5), 5)
        pygame.draw.line(SCREEN, BLACK, (WIDTH//2 - 25, head_y - 30), (WIDTH//2 + 25, head_y - 28), 4)

        # Stitches
        for i in range(6):
            stitch_y = body_rect.top + 20 + i * 30
            pygame.draw.line(SCREEN, BLACK, (WIDTH//2 - 30, stitch_y), (WIDTH//2 + 30, stitch_y), 3)

        pygame.display.flip()

    return STATE_ENDING, choice

def ending_scene(choice):
    timer = 0
    duration = 7000
    hugging = choice == "KISS"
    particles = []

    while timer < duration:
        dt = CLOCK.tick(60)
        timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill(BLACK)

        if hugging:
            # Heart particles
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

            # Messages
            msg1 = FONT_BIG.render("💋 True Love's Kiss! 🧟", True, PINK_LIGHT)
            SCREEN.blit(msg1, msg1.get_rect(center=(WIDTH//2, 90)))

            msg2 = FONT_MED.render("He wakes and embraces you!", True, WHITE)
            SCREEN.blit(msg2, msg2.get_rect(center=(WIDTH//2, 150)))

            msg3 = FONT_BIG.render("💕 Happy Creepy Valentine! 💕", True, MARIO_RED)
            SCREEN.blit(msg3, msg3.get_rect(center=(WIDTH//2, HEIGHT - 80)))

            # Hugging couple
            girl_x, boy_x = WIDTH//2 - 80, WIDTH//2 + 40
            y = HEIGHT//2 - 30

            # Girl
            pygame.draw.rect(SCREEN, PINK_LIGHT, (girl_x, y, 50, 100), 0, 15)
            pygame.draw.circle(SCREEN, MARIO_SKIN, (girl_x + 25, y - 25), 25)
            pygame.draw.rect(SCREEN, PINK, (girl_x + 8, y + 35, 34, 65), 0, 12)
            pygame.draw.circle(SCREEN, BLACK, (girl_x + 18, y - 28), 3)
            pygame.draw.circle(SCREEN, BLACK, (girl_x + 32, y - 28), 3)

            # Boy
            pygame.draw.rect(SCREEN, GREEN_ZOMBIE, (boy_x, y, 50, 100), 0, 15)
            pygame.draw.circle(SCREEN, GREEN_ZOMBIE, (boy_x + 25, y - 25), 25)
            pygame.draw.line(SCREEN, BLACK, (boy_x + 10, y - 35), (boy_x + 40, y - 33), 4)
            pygame.draw.circle(SCREEN, BLACK, (boy_x + 18, y - 28), 3)
            pygame.draw.circle(SCREEN, BLACK, (boy_x + 32, y - 28), 3)

            # Hug arms
            pygame.draw.line(SCREEN, PINK_LIGHT, (girl_x + 50, y + 35), (boy_x + 10, y + 45), 14)
            pygame.draw.line(SCREEN, GREEN_ZOMBIE, (boy_x, y + 35), (girl_x + 40, y + 45), 14)

            # Orbiting hearts
            angle = timer / 15
            for i in range(10):
                a = angle + i * 36
                rad = math.radians(a)
                hx = WIDTH//2 + math.cos(rad) * 140
                hy = HEIGHT//2 + math.sin(rad) * 90
                draw_heart(SCREEN, (int(hx), int(hy)), RED, 14)

        else:
            # Lightning ending
            msg1 = FONT_BIG.render("⚡ Lightning Strike! ⚡", True, YELLOW)
            SCREEN.blit(msg1, msg1.get_rect(center=(WIDTH//2, 90)))

            msg2 = FONT_MED.render("The spark fades... he remains still. 💔", True, WHITE)
            SCREEN.blit(msg2, msg2.get_rect(center=(WIDTH//2, 150)))

            # Dead body
            pygame.draw.rect(SCREEN, GREY, (WIDTH//2 - 60, HEIGHT//2 - 110, 120, 200), 0, 18)
            pygame.draw.circle(SCREEN, GREY, (WIDTH//2, HEIGHT//2 - 130), 40)

            # X eyes
            for x_off in [-20, 20]:
                cx = WIDTH//2 + x_off
                pygame.draw.line(SCREEN, BLACK, (cx-8, HEIGHT//2-140), (cx+8, HEIGHT//2-120), 4)
                pygame.draw.line(SCREEN, BLACK, (cx+8, HEIGHT//2-140), (cx-8, HEIGHT//2-120), 4)

            # Animated lightning
            if timer % 600 < 300:
                points = [(WIDTH//2 - 180, 0)]
                y = 0
                x = WIDTH//2 - 180
                for _ in range(8):
                    x += random.randint(-30, 30)
                    y += random.randint(60, 100)
                    points.append((x, y))
                pygame.draw.lines(SCREEN, YELLOW, False, points, 5)
                pygame.draw.lines(SCREEN, WHITE, False, points, 2)

        pygame.display.flip()

    return ending_menu()

def ending_menu():
    play_again_btn = Button((WIDTH//2 - 310, HEIGHT//2 + 50, 280, 90), "🔄 Play Again")
    quit_btn = Button((WIDTH//2 + 30, HEIGHT//2 + 50, 280, 90), "🚪 Quit", GREY, (90, 90, 100))

    while True:
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

        # Gradient background
        for y in range(0, HEIGHT, 2):
            shade = int(20 + (y / HEIGHT) * 40)
            pygame.draw.line(SCREEN, (shade, shade, shade + 10), (0, y), (WIDTH, y))

        # Title
        msg = FONT_BIG.render("Experiment Complete", True, GREEN_ZOMBIE)
        SCREEN.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2 - 100)))

        sub = FONT_MED.render("Will you try again?", True, PINK)
        SCREEN.blit(sub, sub.get_rect(center=(WIDTH//2, HEIGHT//2 - 30)))

        play_again_btn.draw(SCREEN)
        quit_btn.draw(SCREEN)

        pygame.display.flip()

# ------------------------- MAIN -------------------------
def main():
    start_music()
    state = STATE_TITLE
    choice = None

    while True:
        if state == STATE_TITLE:
            state = title_scene()
        elif state == STATE_STAGE1:
            state = stage1_scene()
        elif state == STATE_STAGE2:
            state = stage2_scene()
        elif state == STATE_STAGE3:
            state, choice = stage3_scene()
        elif state == STATE_ENDING:
            state = ending_scene(choice)

if __name__ == "__main__":
    main()
