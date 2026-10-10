from ursina import *
import random

# Initialize Ursina App
app = Ursina()

# Window Setup
window.title = "The Homeless Hustle 3D - Human Edition"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False

# Lighting and Atmosphere
Entity(type='directional light', rotation=(45, -45, 0))
sky = Sky(color=color.rgb(110, 130, 160))

# Ground (The Main Street)
ground = Entity(model='plane', scale=(200, 1, 200), color=color.dark_gray, texture='white_cube', collider='box')

# --- GENERATE A FULL 3D CITY ---
for z in range(-60, 90, 20):
    Entity(model='cube', scale=(12, random.uniform(25, 45), 12), position=(-22, 10, z), color=color.rgb(65, 70, 80))
    Entity(model='cube', scale=(12, random.uniform(15, 30), 12), position=(-36, 10, z), color=color.rgb(55, 60, 70))
    Entity(model='cube', scale=(12, random.uniform(25, 45), 12), position=(22, 10, z), color=color.rgb(70, 65, 80))
    Entity(model='cube', scale=(12, random.uniform(15, 30), 12), position=(36, 10, z), color=color.rgb(60, 55, 70))

# Game State Variables
quests_completed = 0
TOTAL_QUESTS = 50
money = 0
MAX_STAMINA = 100
stamina = MAX_STAMINA
game_over = False
quest_state = "GET_QUEST" 
target_pos = Vec3(0, 0, 0)
police_chasing = False
death_screen = []
play_again_button = None

# Target Marker
quest_marker = Entity(model='cube', color=color.yellow, scale=(1.5, 3, 1.5), position=(0, 1.5, 0), enabled=False)

# --- DETAILED HUMANOID HOMELESS PLAYER MODEL ---
player = Entity(position=(0, 0, 0))
player.collider = BoxCollider(player, center=(0, 1, 0), size=(0.8, 2, 0.8))

# Head & Face
p_head = Entity(parent=player, model='sphere', scale=(0.3, 0.35, 0.3), color=color.rgb(210, 170, 140), y=1.75)
p_hair = Entity(parent=player, model='cube', scale=(0.35, 0.15, 0.35), color=color.rgb(50, 40, 30), y=1.9)
# Torso (Tattered Hoodie)
p_torso = Entity(parent=player, model='cube', scale=(0.55, 0.7, 0.3), color=color.rgb(100, 80, 50), y=1.2)
# Cardboard Sign on Chest
p_sign = Entity(parent=player, model='cube', scale=(0.5, 0.35, 0.05), color=color.rgb(190, 150, 100), z=-0.17, y=1.25)
# Arms
p_arm_l = Entity(parent=player, model='cube', scale=(0.15, 0.6, 0.15), color=color.rgb(90, 70, 45), x=-0.38, y=1.2)
p_arm_r = Entity(parent=player, model='cube', scale=(0.15, 0.6, 0.15), color=color.rgb(90, 70, 45), x=0.38, y=1.2)
# Legs (Torn Jeans)
p_leg_l = Entity(parent=player, model='cube', scale=(0.2, 0.7, 0.2), color=color.rgb(50, 70, 100), x=-0.15, y=0.45)
p_leg_r = Entity(parent=player, model='cube', scale=(0.2, 0.7, 0.2), color=color.rgb(50, 70, 100), x=0.15, y=0.45)

# --- HUMANOID GANG BOSS NPC ---
gang_boss = Entity(position=(0, 0, 10))
gang_boss.collider = BoxCollider(gang_boss, center=(0, 1, 0), size=(0.8, 2, 0.8))

b_head = Entity(parent=gang_boss, model='sphere', scale=(0.3, 0.35, 0.3), color=color.rgb(230, 190, 150), y=1.75)
b_torso = Entity(parent=gang_boss, model='cube', scale=(0.6, 0.75, 0.3), color=color.rgb(180, 20, 20), y=1.2) # Sharp Suit Jacket
b_arm_l = Entity(parent=gang_boss, model='cube', scale=(0.15, 0.6, 0.15), color=color.rgb(150, 10, 10), x=-0.4, y=1.2)
b_arm_r = Entity(parent=gang_boss, model='cube', scale=(0.15, 0.6, 0.15), color=color.rgb(150, 10, 10), x=0.4, y=1.2)
b_leg_l = Entity(parent=gang_boss, model='cube', scale=(0.2, 0.75, 0.2), color=color.rgb(20, 20, 20), x=-0.15, y=0.45)
b_leg_r = Entity(parent=gang_boss, model='cube', scale=(0.2, 0.75, 0.2), color=color.rgb(20, 20, 20), x=0.15, y=0.45)
boss_label = Text(text="Gang Boss", position=(-0.05, 0.1), scale=1, billboard=True, parent=gang_boss)

# --- POLICE CHASE NPC ---
police = Entity(position=(0, 0, -12))
police.collider = BoxCollider(police, center=(0, 1, 0), size=(0.8, 2, 0.8))
police.enabled = False

police_head = Entity(parent=police, model='sphere', scale=(0.3, 0.35, 0.3), color=color.rgb(200, 210, 220), y=1.75)
police_torso = Entity(parent=police, model='cube', scale=(0.6, 0.75, 0.3), color=color.rgb(30, 60, 120), y=1.2)
police_arm_l = Entity(parent=police, model='cube', scale=(0.15, 0.6, 0.15), color=color.rgb(180, 180, 180), x=-0.4, y=1.2)
police_arm_r = Entity(parent=police, model='cube', scale=(0.15, 0.6, 0.15), color=color.rgb(180, 180, 180), x=0.4, y=1.2)
police_leg_l = Entity(parent=police, model='cube', scale=(0.2, 0.75, 0.2), color=color.rgb(35, 35, 35), x=-0.15, y=0.45)
police_leg_r = Entity(parent=police, model='cube', scale=(0.2, 0.75, 0.2), color=color.rgb(35, 35, 35), x=0.15, y=0.45)
police_label = Text(text="Police", position=(-0.05, 0.1), scale=1, billboard=True, parent=police)

# --- CAMERA PIVOT FOR MOUSE LOOK ---
camera_pivot = Entity(parent=player, y=1.5)
camera.parent = camera_pivot
camera.position = (0, 2, -10)
camera.rotation = (15, 0, 0)

# UI / HUD Text
ui_money = Text(text="Money: $0", position=(-0.85, 0.45), scale=1.5, color=color.green)
ui_quests = Text(text="Quests Completed: 0 / 10000", position=(-0.85, 0.38), scale=1.5, color=color.white)
stamina_label = Text(text="Stamina", position=(-0.85, 0.31), scale=0.8, color=color.white)
stamina_bar_bg = Entity(parent=camera.ui, model='quad', position=(-0.68, 0.32), scale=(0.3, 0.025), color=color.dark_gray)
stamina_bar = Entity(parent=camera.ui, model='quad', position=(-0.83, 0.32, -0.01), scale=(0.3, 0.025), color=color.green)
ui_instructions = Text(text="[W/A/S/D] Move | [SHIFT] Sprint | [Mouse] Look Around | [SPACE] Interact", position=(-0.6, -0.4), scale=1.0, color=color.yellow)

# Game Update Loop
def update():
    global money, quests_completed, game_over, quest_state, police_chasing, stamina

    if game_over:
        return

    # Movement Speeds
    move_speed = 7 * time.dt
    is_moving = any(held_keys[key] for key in ('w', 'a', 's', 'd'))
    sprint_requested = held_keys['shift'] or held_keys['left shift'] or held_keys['right shift']
    is_sprinting = sprint_requested and is_moving and stamina > 0
    if is_sprinting:
        move_speed *= 2.0

    # Player Movement controls
    if held_keys['w']:
        player.z += move_speed
    if held_keys['s']:
        player.z -= move_speed
    if held_keys['a']:
        player.x -= move_speed
    if held_keys['d']:
        player.x += move_speed

    if is_sprinting:
        stamina = max(0, stamina - 35 * time.dt)
    else:
        stamina = min(MAX_STAMINA, stamina + 22 * time.dt)
    stamina_fraction = stamina / MAX_STAMINA
    stamina_bar.scale_x = 0.3 * stamina_fraction
    stamina_bar.x = -0.83 + 0.15 * stamina_fraction
    stamina_bar.color = color.green if stamina_fraction > 0.5 else color.yellow if stamina_fraction > 0.2 else color.red

    # Smooth Mouse Look Rotation around the Pivot
    camera_pivot.rotation_y += mouse.velocity[0] * 40
    camera_pivot.rotation_x -= mouse.velocity[1] * 40
    camera_pivot.rotation_x = clamp(camera_pivot.rotation_x, -15, 45)

    # Quest distance logic
    distance_to_boss = distance_xz(player.position, gang_boss.position)
    distance_to_target = distance_xz(player.position, quest_marker.position) if quest_marker.enabled else 999

    if quest_state == "GET_QUEST":
        police.enabled = False
        police_chasing = False
        if distance_to_boss < 3:
            ui_instructions.text = "Press [SPACE] to accept a shady task from the Gang Boss!"
        else:
            ui_instructions.text = "Walk/Sprint back to the Gang Boss. Move mouse to look around."
    elif quest_state == "GO_TO_TARGET":
        police.enabled = True
        police_chasing = True

        if distance_xz(police.position, player.position) > 12:
            police.position = player.position + Vec3(0, 0, -12)

        chase_dir = player.position - police.position
        chase_dir.y = 0
        if distance_xz(player.position, police.position) > 0.1:
            police.position += chase_dir.normalized() * (5.5 * time.dt)

        if distance_xz(player.position, police.position) < 2.2:
            trigger_death()

        if distance_to_target < 3:
            ui_instructions.text = "You reached the destination! Press [SPACE] to complete the task."
        else:
            ui_instructions.text = "Sprint down the city street to the yellow marker!"

# Key Input Handler
def input(key):
    global money, quests_completed, game_over, quest_state, target_pos, police_chasing

    if key == 'space' and not game_over:
        distance_to_boss = distance_xz(player.position, gang_boss.position)
        distance_to_target = distance_xz(player.position, quest_marker.position) if quest_marker.enabled else 999

        if quest_state == "GET_QUEST" and distance_to_boss < 3:
            random_x = random.choice([-15, 15])
            random_z = random.randint(-40, 70)
            target_pos = Vec3(random_x, 1.5, random_z)

            quest_marker.position = target_pos
            quest_marker.enabled = True
            police.position = player.position + Vec3(0, 0, -12)
            police.enabled = True
            police_chasing = True
            quest_state = "GO_TO_TARGET"
            ui_instructions.text = "Trip started! Sprint to the yellow marker in the city while the police chase you."

        elif quest_state == "GO_TO_TARGET" and distance_to_target < 3:
            quests_completed += 1
            money += 50
            ui_money.text = f"Money: ${money}"
            ui_quests.text = f"Quests Completed: {quests_completed} / {TOTAL_QUESTS}"

            quest_marker.enabled = False
            police.enabled = False
            police_chasing = False
            quest_state = "GET_QUEST"

            if quests_completed >= TOTAL_QUESTS:
                trigger_ending()
            else:
                ui_instructions.text = "Quest complete! Return to the Gang Boss for another one."


def trigger_death():
    global game_over, death_screen, play_again_button
    game_over = True

    player.disable()
    gang_boss.disable()
    police.disable()
    quest_marker.disable()
    ui_money.disable()
    ui_quests.disable()
    stamina_label.disable()
    stamina_bar_bg.disable()
    stamina_bar.disable()
    ui_instructions.disable()

    sky.color = color.black
    death_screen = [
        Text(text="YOU GOT CAUGHT BY THE POLICE!", position=(-0.45, 0.2), scale=2, color=color.red),
        Text(text="The sirens were too loud and the chase ended in your death.", position=(-0.55, 0.0), scale=1.1, color=color.white),
        Text(text=f"Quests Completed: {quests_completed}", position=(-0.45, -0.15), scale=1.2, color=color.yellow),
    ]
    play_again_button = Button(text="Play Again", position=(0, -0.3), scale=(0.2, 0.08), on_click=restart_game)


def restart_game():
    global money, quests_completed, game_over, quest_state, target_pos, police_chasing
    global death_screen, play_again_button, stamina

    for item in death_screen:
        destroy(item)
    death_screen = []
    destroy(play_again_button)
    play_again_button = None

    money = 0
    stamina = MAX_STAMINA
    quests_completed = 0
    game_over = False
    quest_state = "GET_QUEST"
    target_pos = Vec3(0, 0, 0)
    police_chasing = False

    player.enable()
    player.position = Vec3(0, 0, 0)
    player.rotation = Vec3(0, 0, 0)
    camera_pivot.rotation = Vec3(0, 0, 0)
    gang_boss.enable()
    police.disable()
    police.position = Vec3(0, 0, -12)
    quest_marker.disable()
    quest_marker.position = Vec3(0, 1.5, 0)
    sky.color = color.rgb(110, 130, 160)

    ui_money.enable()
    ui_money.text = "Money: $0"
    ui_quests.enable()
    ui_quests.text = f"Quests Completed: 0 / {TOTAL_QUESTS}"
    stamina_label.enable()
    stamina_bar_bg.enable()
    stamina_bar.enable()
    stamina_bar.scale_x = 0.3
    stamina_bar.x = -0.68
    stamina_bar.color = color.green
    ui_instructions.enable()
    ui_instructions.text = "[W/A/S/D] Move | [SHIFT] Sprint | [Mouse] Look Around | [SPACE] Interact"


def trigger_ending():
    global game_over
    game_over = True

    player.disable()
    gang_boss.disable()
    police.disable()
    quest_marker.disable()
    ui_money.disable()
    ui_quests.disable()
    stamina_label.disable()
    stamina_bar_bg.disable()
    stamina_bar.disable()
    ui_instructions.disable()

    Sky(color=color.black)
    Text(text="YOU COMPLETED ALL 10,000 QUESTS!", position=(-0.4, 0.2), scale=2, color=color.red)
    Text(text="The gang tricked you all along and eliminated you to keep the money.", position=(-0.4, 0.0), scale=1.2, color=color.white)
    Text(text=f"Final Money: ${money} (Useless now)", position=(-0.4, -0.1), scale=1.2, color=color.green)

app.run()