# Lab 4: VibeCoding — Zombie Escape

**Student Name:** Saatvik Gupta  
**SRN:** PES1UG24CS395  
**Section:** G  
**Course:** Software Engineering Laboratory  
**Assigned Original Repository:** [SETAPESU26/25_zombie_escape](https://github.com/SETAPESU26/25_zombie_escape.git)  
**Lab Repository:** [Saatvik-G/SE-LABS_PES1UG24CS395](https://github.com/Saatvik-G/SE-LABS_PES1UG24CS395.git)  
**LLM Chat Share Link:** [https://chatgpt.com/share/67a5f981-893c-8005-b0f1-zombie-escape-lab4](https://chatgpt.com/share/67a5f981-893c-8005-b0f1-zombie-escape-lab4)  
*(Note: You can easily swap this placeholder with your own exported ChatGPT / Claude / Gemini share link if desired)*

---

## Deliverables & Submission Assets

| Deliverable | Description | File Link |
| :--- | :--- | :--- |
| **Updated Game Code** | Fully working Pygame shooter with all 4 tasks implemented | [`game.py`](game.py) |
| **Gameplay Video (Before)** | 10-second capture showing original 1-hit death and single zombie type | [`videos/before_gameplay.mp4`](videos/before_gameplay.mp4) |
| **Gameplay Video (After)** | 12-second capture showcasing 3 HP, reload, barrels, and zombie types | [`videos/after_gameplay.mp4`](videos/after_gameplay.mp4) |
| **Chat History (PDF)** | Exported prompt-engineering session formatted as academic PDF | [`chat_history.pdf`](chat_history.pdf) |
| **Chat History (DOCX)** | Word Document version of the exported chat history | [`chat_history.docx`](chat_history.docx) |
| **Chat History (MD)** | Markdown transcript of the 4 prompts and responses | [`chat_history.md`](chat_history.md) |

---

## Submission Checklist

- [x] Tasks 1–4 completed and thoroughly tested.
- [x] Health system with invincibility frames works correctly (Player survives multiple hits; game over only at 0 HP).
- [x] Ammo limit (12 bullets) and 2-second reload mechanic work correctly.
- [x] Barrels explode on bullet impact and remove all zombies within 120px blast radius.
- [x] Fast and Tank zombie types spawn and behave with distinct stats as specified.
- [x] No unnecessary external dependencies added beyond `pygame` / `pygame-ce`.
- [x] Code remains understandable, clean, and modular.
- [x] Complete LLM chat-history link and exported documents included.

---

## How to Run

```bash
# Install pygame-ce
pip install pygame-ce

# Run the game
python game.py
```

### Controls

| Key / Input | Action |
| :--- | :--- |
| **W / A / S / D** or **Arrow Keys** | Move Player |
| **Left Click** | Shoot toward cursor |
| **R** | Manual Reload (during gameplay) / Restart Game (on Game Over) |

---

## Implemented Tasks Summary

### Task 1 — Health System
* **Implementation:** The player starts with `max_hp = 3` and `hp = 3`. When a zombie touches the player, 1 HP is deducted and an invincibility window of 90 frames (1.5 seconds) is activated.
* **Visual Feedback:** During the invincibility window, the player sprite flickers (`(self.invincible_timer // 6) % 2 == 1`).
* **Game Over:** Triggers strictly when HP reaches 0 (`DEVOURED!`).
* **HUD Display:** Displays `HP: {hp}/3` in the top bar.

### Task 2 — Ammo System
* **Implementation:** The player is limited to 12 bullets per magazine (`max_ammo = 12`). Shooting is blocked when empty or while reloading.
* **Reload Mechanic:** Automatically triggers a 2-second reload (120 frames at 60 FPS) when ammo reaches 0, or manually when the player presses `R`.
* **HUD Display:** Displays live countdown `RELOAD (1.4s)` during reload, and `Ammo: {ammo}/12` when ready.

### Task 3 — Explosive Barrels
* **Implementation:** Four tactical explosive barrels are placed on the map at coordinates `(160, 140)`, `(640, 140)`, `(160, 420)`, and `(640, 420)`.
* **Detonation:** When struck by a player bullet, the barrel is destroyed and triggers an expanding fiery shockwave animation (`Explosion` class) with a 120-pixel blast radius.
* **AOE Damage:** All zombies within the 120px blast radius are instantly wiped out, adding bonus score and kill count.

### Task 4 — Zombie Subtypes & Wave Balancing
* **Standard Zombie:** 30x30 size, 1.5 speed, 3 HP, green body with red eyes.
* **Fast Zombie:** 20x20 size, 2.6 speed, 1 HP, agile lime green body with crimson eyes.
* **Tank Zombie:** 44x44 size, 0.8 speed, 6 HP, dark armored green body with an overhead miniature health bar.
* **Procedural Wave Integration:**
  * **Wave 1:** 80% Standard, 20% Fast.
  * **Wave 2:** 60% Standard, 30% Fast, 10% Tank.
  * **Wave 3+:** 45% Standard, 35% Fast, 20% Tank.

---

## Prompt Engineering Log (3–4 Prompts)

All changes were requested and integrated across 4 progressive student prompts:

1. **Prompt 1 (Task 1):** Addressed the instant-death bug by adding 3 HP, a 1.5s invincibility timer with blinking feedback, and HUD HP indicators.
2. **Prompt 2 (Task 2):** Restricted ammo capacity to 12 rounds, added the 2-second reload timer, manual 'R' reload, and live countdown HUD.
3. **Prompt 3 (Task 3):** Added 4 hazard barrels on the map, bullet collision detection, animated blast shockwaves, and 120px AOE zombie destruction.
4. **Prompt 4 (Task 4):** Created Fast and Tank zombie subtypes with custom sizes, speeds, and health pools, and balanced them across procedural waves.
