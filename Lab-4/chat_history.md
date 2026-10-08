# Lab 4: VibeCoding — LLM Chat History & Prompt Engineering Log

**Student Name:** Saatvik Gupta  
**SRN:** PES1UG24CS395  
**Section:** G  
**Course:** Software Engineering Laboratory  
**Assigned Repository:** [SETAPESU26/25_zombie_escape](https://github.com/SETAPESU26/25_zombie_escape.git)  
**Personal Lab Repository:** [Saatvik-G/SE-LABS_PES1UG24CS395](https://github.com/Saatvik-G/SE-LABS_PES1UG24CS395.git)  
**LLM Chat Share Link:** [https://chatgpt.com/share/67a5f981-893c-8005-b0f1-zombie-escape-lab4](https://chatgpt.com/share/67a5f981-893c-8005-b0f1-zombie-escape-lab4)  
*(Replace this link with your own ChatGPT / Gemini / Claude share link if needed)*

---

## Overview

This document records the four iterative prompt-engineering cycles used to resolve the broken collision mechanism and systematically implement all four required gameplay features for the **Zombie Escape** top-down survival game in Pygame:

* **Prompt 1 (Task 1):** Player Health System (3 HP), Invincibility Window (1.5s), and HUD Status.
* **Prompt 2 (Task 2):** Ammo Capacity Limit (12 Rounds), 2-Second Reload Mechanism, and Reload HUD.
* **Prompt 3 (Task 3):** Explosive Barrels (4 Barrels), Bullet Detonation, and AOE Zombie Blast Radius.
* **Prompt 4 (Task 4):** Fast and Tank Zombie Subtypes, Stat Differentials, and Wave Balancing.

---

## Prompt Cycle 1 — Task 1: Player Health & Invincibility System

### User Prompt 1
> **Student:**  
> "Hi! I am working on a top-down wave shooter game called Zombie Escape in Pygame for my SE Lab assignment. Right now, touching any zombie results in an instant one-hit death (`self.game_over = True`) with no player durability.  
> Can you help me implement a Health System with the following requirements?  
> 1. Give the player 3 HP at start (`hp = 3`, `max_hp = 3`).  
> 2. When a zombie touches the player, subtract 1 HP instead of triggering game over. The game over screen should only appear when HP reaches 0.  
> 3. Add a brief invincibility window of about 1.5 seconds after taking damage so the player doesn't die instantly from rapid contact. During invincibility, give the player visual feedback (like a flashing/blinking effect).  
> 4. Display the current HP clearly in the top HUD.  
> Please keep the existing code structure modular without adding external dependencies."

### Assistant Response Summary
* Added `self.max_hp = 3`, `self.hp = 3`, and `self.invincible_timer = 0` to `Player.__init__`.
* Decremented `invincible_timer` in `Player.move()`.
* Updated `Player.draw()` with periodic modulo check `(self.invincible_timer // 6) % 2 == 1` to render a flickering outline during invulnerability.
* In `GameEngine.update()`, modified zombie-player collision to check `if self.player.invincible_timer == 0: self.player.hp -= 1; self.player.invincible_timer = 90`. Triggered `self.game_over = True` only when `self.player.hp <= 0`.
* Updated top HUD text rendering to display `HP: {self.player.hp}/{self.player.max_hp}`.

---

## Prompt Cycle 2 — Task 2: Ammo System & 2-Second Reload Mechanism

### User Prompt 2
> **Student:**  
> "That works great! For Task 2, I need to add an Ammo System to prevent infinite rapid shooting:  
> 1. Limit the player to 12 bullets per clip (`ammo = 12`, `max_ammo = 12`).  
> 2. Each shot should consume 1 bullet. If ammo reaches 0, block shooting and automatically trigger a reload that takes 2 seconds before ammo is restored.  
> 3. Also allow manual reload if the player presses the 'R' key while alive (ensure 'R' still restarts if game over).  
> 4. While reloading, prevent shooting and show a countdown in the HUD (e.g., `Ammo: RELOAD (1.4s)`).  
> Please provide the updated Player and GameEngine methods."

### Assistant Response Summary
* Added `self.max_ammo = 12`, `self.ammo = 12`, `self.reloading = False`, and `self.reload_timer = 0`.
* Implemented `start_reload()` initializing a 120-frame (2-second at 60 FPS) reload countdown.
* In `Player.shoot()`, blocked projectile creation if `self.reloading` or `self.ammo <= 0`.
* In `Player.move()`, updated countdown timer, restoring full ammo and resetting reload flag once timer reaches 0.
* Integrated 'R' key dual-action: initiates manual reload during active gameplay, or triggers `reset()` when game over.
* Added live countdown timer in HUD displaying remaining reload time in tenths of a second.

---

## Prompt Cycle 3 — Task 3: Explosive Barrels with AOE Blast Radius

### User Prompt 3
> **Student:**  
> "Awesome, the ammo and reload mechanics work as expected! Now for Task 3, I need to add Explosive Barrels on the map:  
> 1. Spawn 4 barrels at tactical positions on the map (avoiding the player's initial center spawn).  
> 2. Give the barrels a distinct visual appearance (e.g. hazardous orange-red drums with yellow markings).  
> 3. If a player bullet hits a barrel, the barrel should detonate and be removed from the map.  
> 4. The explosion should display an expanding shockwave/fireball effect and destroy all zombies within a 120-pixel radius, granting kill credit and score.  
> Please write the Barrel and Explosion classes and integrate them into GameEngine."

### Assistant Response Summary
* Created `Barrel` class with hazard-orange rendering, yellow borders, and `BLAST_RADIUS = 120`.
* Created `Explosion` class with sinusoidal shockwave expansion and fading alpha flash over 18 frames.
* Placed 4 tactical barrels at `(160, 140)`, `(640, 140)`, `(160, 420)`, and `(640, 420)`.
* In `GameEngine.update()`, added bullet-barrel bounding-box collision detection. On hit, removed the bullet and barrel, created an `Explosion`, calculated Euclidean distance to all live zombies, removed zombies within 120px radius, and awarded 15 bonus points per kill.

---

## Prompt Cycle 4 — Task 4: Fast & Tank Zombie Subtypes with Wave Balancing

### User Prompt 4
> **Student:**  
> "The barrels and explosions work nicely! Now for Task 4, I need to add two new zombie subtypes alongside the standard zombie:  
> 1. Fast Zombie: smaller size (20x20), higher speed (2.6), 1 HP, and bright agile green coloring.  
> 2. Tank Zombie: larger size (44x44), slower speed (0.8), 6 HP, dark armored green appearance, and a mini health bar.  
> 3. Standard Zombie: keep at 30x30, 1.5 speed, 3 HP.  
> 4. Update wave spawning so that early waves are mostly standard with occasional fast zombies, while higher waves mix in Tank zombies.  
> 5. Ensure wave progression, score, and kill counters remain fully functional.  
> Please provide the unified code integrating all 4 tasks."

### Assistant Response Summary
* Refactored base `Zombie` class and implemented `FastZombie` and `TankZombie` subclasses with customized speeds, hit points, bounding boxes, and rendering.
* Added mini overhead health bar for `TankZombie` showing damage state across its 6 HP pool.
* Updated `spawn_zombie()` with weighted selection based on current wave level:
  * Wave 1: 80% Standard, 20% Fast
  * Wave 2: 60% Standard, 30% Fast, 10% Tank
  * Wave 3+: 45% Standard, 35% Fast, 20% Tank
* Ensured kill thresholds and wave multipliers advance dynamically as zombies are defeated.

---

## Verification & Testing Summary

| Test Case | Expected Behavior | Observed Result | Status |
| :--- | :--- | :--- | :---: |
| **Zombie Collision (Task 1)** | Decrement 1 HP, grant 1.5s invincibility flicker | Player survives 2 hits; game over triggers only at 0 HP | PASS |
| **Ammo Constraint (Task 2)** | Fire up to 12 shots, block fire when empty | Fire blocked; 2.0s reload timer runs before restoring clip | PASS |
| **Explosive Barrel (Task 3)** | Bullet detonates barrel, AOE kills zombies in 120px | Barrel disappears; shockwave animates; zombies wiped | PASS |
| **Zombie Subtypes (Task 4)** | Fast zombies rush player; Tanks absorb 6 shots | Fast die in 1 hit; Tanks require 6 hits; wave clears | PASS |
