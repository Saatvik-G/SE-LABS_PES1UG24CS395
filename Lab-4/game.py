import pygame
import random
import math
import time

WIDTH, HEIGHT = 800, 560
FPS = 60
BG = (30,35,25)


class Zombie:
    SPEED = 1.5

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = (60,140,60)
        self.hp = 3
        self.wobble = random.uniform(0, 6.28)
        self.frame = 0

    def update(self, player_pos):
        px, py = player_pos
        cx, cy = self.rect.center
        dx, dy = px-cx, py-cy
        dist = (dx**2+dy**2)**0.5
        if dist:
            self.rect.x += int(dx/dist*self.SPEED)
            self.rect.y += int(dy/dist*self.SPEED)
        self.frame += 1

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

    def draw(self, screen):
        wobble_y = int(math.sin(self.frame*0.2)*3)
        draw_rect = self.rect.move(0, wobble_y)
        pygame.draw.rect(screen, self.color, draw_rect, border_radius=5)
        for ex in [draw_rect.x+6, draw_rect.x+18]:
            pygame.draw.circle(screen, (200,40,40), (ex, draw_rect.y+10), 4)


def spawn_zombie(width, height, player_rect, margin=120):
    while True:
        x = random.randint(0, width-30)
        y = random.randint(0, height-30)
        rect = pygame.Rect(x, y, 30, 30)
        if not rect.colliderect(player_rect.inflate(margin, margin)):
            return Zombie(x, y)


# Task 3: Explosive Barrel and Explosion classes
class Barrel:
    RADIUS = 16
    BLAST_RADIUS = 120

    def __init__(self, x, y):
        self.rect = pygame.Rect(x - self.RADIUS, y - self.RADIUS, self.RADIUS * 2, self.RADIUS * 2)
        self.color = (210, 75, 20)

    def draw(self, screen):
        # Draw barrel with metal drum ridges and yellow hazard indicator
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        pygame.draw.rect(screen, (245, 185, 30), self.rect, width=2, border_radius=6)
        cx, cy = self.rect.center
        pygame.draw.line(screen, (30, 25, 20), (cx - 10, cy), (cx + 10, cy), 3)
        pygame.draw.circle(screen, (255, 235, 80), (cx, cy), 4)


class Explosion:
    def __init__(self, x, y, max_radius=120, duration=18):
        self.x = x
        self.y = y
        self.max_radius = max_radius
        self.duration = duration
        self.frame = 0

    def update(self):
        self.frame += 1
        return self.frame >= self.duration

    def draw(self, screen):
        progress = self.frame / self.duration
        current_r = max(4, int(self.max_radius * math.sin(progress * math.pi / 2)))
        alpha = int(255 * (1 - progress))
        surf = pygame.Surface((self.max_radius * 2 + 20, self.max_radius * 2 + 20), pygame.SRCALPHA)
        center = (self.max_radius + 10, self.max_radius + 10)
        # Outer shockwave ring
        ring_width = max(2, int(6 * (1 - progress)))
        pygame.draw.circle(surf, (255, 110, 20, max(0, min(255, alpha))), center, current_r, width=ring_width)
        # Inner flash
        inner_r = max(2, int(current_r * 0.65))
        pygame.draw.circle(surf, (255, 220, 50, max(0, min(255, int(alpha * 0.75)))), center, inner_r)
        screen.blit(surf, (self.x - self.max_radius - 10, self.y - self.max_radius - 10))


SPEED = 4


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = (60,160,220)
        self.bullets = []
        self.shoot_cooldown = 0
        # Task 1: Health & Invincibility
        self.max_hp = 3
        self.hp = 3
        self.invincible_timer = 0
        # Task 2: Ammo & 2-second Reload System
        self.max_ammo = 12
        self.ammo = 12
        self.reloading = False
        self.reload_timer = 0

    def start_reload(self):
        if not self.reloading and self.ammo < self.max_ammo:
            self.reloading = True
            self.reload_timer = 2 * FPS

    def move(self, keys, width, height):
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]: dy = -SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy = SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx = -SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = SPEED
        self.rect.x = max(0, min(width-self.rect.width, self.rect.x+dx))
        self.rect.y = max(0, min(height-self.rect.height, self.rect.y+dy))
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self.reloading:
            self.reload_timer -= 1
            if self.reload_timer <= 0:
                self.ammo = self.max_ammo
                self.reloading = False
                self.reload_timer = 0

    def shoot(self, target_pos):
        if self.shoot_cooldown > 0: return
        if self.reloading: return
        if self.ammo <= 0:
            self.start_reload()
            return

        cx, cy = self.rect.center
        tx, ty = target_pos
        dx, dy = tx-cx, ty-cy
        dist = (dx**2+dy**2)**0.5
        if dist == 0: return
        vx, vy = dx/dist*10, dy/dist*10
        self.bullets.append([cx-4, cy-4, vx, vy])
        self.shoot_cooldown = 15
        self.ammo -= 1
        if self.ammo <= 0:
            self.start_reload()

    def update_bullets(self, width, height):
        live = []
        for b in self.bullets:
            b[0] += b[2]; b[1] += b[3]
            if 0 <= b[0] <= width and 0 <= b[1] <= height:
                live.append(b)
        self.bullets = live

    def draw(self, screen):
        if self.invincible_timer > 0 and (self.invincible_timer // 6) % 2 == 1:
            pygame.draw.rect(screen, (150, 220, 255), self.rect, width=2, border_radius=6)
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        for b in self.bullets:
            pygame.draw.circle(screen, (255,220,60), (int(b[0]), int(b[1])), 5)


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Zombie Escape")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 17)
        self.big_font = pygame.font.SysFont("monospace", 44, bold=True)
        self.reset()

    def reset(self):
        self.player = Player(WIDTH//2, HEIGHT//2)
        self.zombies = [spawn_zombie(WIDTH, HEIGHT, self.player.rect) for _ in range(4)]
        # Task 3: 4 Barrels placed on map
        self.barrels = [
            Barrel(160, 140),
            Barrel(640, 140),
            Barrel(160, 420),
            Barrel(640, 420)
        ]
        self.explosions = []
        self.score = 0
        self.wave = 1
        self.kills = 0
        self.kills_to_next = 8
        self.game_over = False
        self.start_time = time.time()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if self.game_over:
                        self.reset()
                    else:
                        self.player.start_reload()
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                self.player.shoot(event.pos)
        return True

    def update(self):
        if self.game_over: return
        keys = pygame.key.get_pressed()
        self.player.move(keys, WIDTH, HEIGHT)
        self.player.update_bullets(WIDTH, HEIGHT)
        self.score = int(time.time() - self.start_time)

        # Update explosions
        self.explosions = [exp for exp in self.explosions if not exp.update()]

        for z in self.zombies:
            z.update(self.player.rect.center)
            if z.rect.colliderect(self.player.rect):
                if self.player.invincible_timer == 0:
                    self.player.hp -= 1
                    self.player.invincible_timer = 90
                    if self.player.hp <= 0:
                        self.game_over = True

        # Task 3: Bullet collision with explosive barrels
        for barrel in self.barrels[:]:
            barrel_hit = False
            for b in self.player.bullets[:]:
                bx, by = int(b[0]), int(b[1])
                if barrel.rect.collidepoint(bx, by):
                    barrel_hit = True
                    if b in self.player.bullets:
                        self.player.bullets.remove(b)
                    break
            if barrel_hit:
                self.barrels.remove(barrel)
                bx, by = barrel.rect.center
                self.explosions.append(Explosion(bx, by, max_radius=barrel.BLAST_RADIUS))
                # Destroy all zombies within blast radius
                for z in self.zombies[:]:
                    zx, zy = z.rect.center
                    dist = ((zx - bx) ** 2 + (zy - by) ** 2) ** 0.5
                    if dist <= barrel.BLAST_RADIUS:
                        self.zombies.remove(z)
                        self.kills += 1
                        self.score += 15

        # Bullet collision with zombies
        dead = []
        for z in self.zombies:
            for b in self.player.bullets[:]:
                bx, by = int(b[0]), int(b[1])
                if z.rect.collidepoint(bx, by):
                    if z.hit():
                        dead.append(z)
                    if b in self.player.bullets:
                        self.player.bullets.remove(b)
        for z in dead:
            if z in self.zombies:
                self.zombies.remove(z)
                self.kills += 1
                self.score += 10

        if self.kills >= self.kills_to_next:
            self.kills = 0
            self.wave += 1
            self.kills_to_next = 8 + self.wave * 2
            for _ in range(self.wave + 3):
                self.zombies.append(spawn_zombie(WIDTH, HEIGHT, self.player.rect))

    def draw(self):
        self.screen.fill(BG)
        for x in range(0, WIDTH, 60):
            pygame.draw.line(self.screen, (40,45,35), (x,0), (x,HEIGHT), 1)
        for y in range(0, HEIGHT, 60):
            pygame.draw.line(self.screen, (40,45,35), (0,y), (WIDTH,y), 1)

        # Task 3: Draw barrels & explosions
        for barrel in self.barrels: barrel.draw(self.screen)
        for exp in self.explosions: exp.draw(self.screen)

        for z in self.zombies: z.draw(self.screen)
        self.player.draw(self.screen)

        hud_bg = pygame.Rect(0, 0, WIDTH, 40)
        pygame.draw.rect(self.screen, (15,20,15), hud_bg)

        if self.player.reloading:
            sec_left = max(0.1, self.player.reload_timer / FPS)
            ammo_str = f"RELOAD ({sec_left:.1f}s)"
        else:
            ammo_str = f"{self.player.ammo}/{self.player.max_ammo}"

        hud = self.font.render(
            f"Wave: {self.wave}  Score: {self.score}  Kills: {self.kills}/{self.kills_to_next}  HP: {self.player.hp}/{self.player.max_hp}  Ammo: {ammo_str}  [R: Reload]",
            True, (160,220,120))
        self.screen.blit(hud, (8, 9))

        if self.game_over:
            ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ov.fill((0,0,0,160))
            self.screen.blit(ov, (0,0))
            m = self.big_font.render("DEVOURED!", True, (180,40,40))
            s = self.font.render(f"Wave {self.wave} | Score {self.score} | Press R to Restart", True, (200,200,200))
            self.screen.blit(m, (WIDTH//2-m.get_width()//2, HEIGHT//2-40))
            self.screen.blit(s, (WIDTH//2-s.get_width()//2, HEIGHT//2+20))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    engine = GameEngine()
    engine.run()
