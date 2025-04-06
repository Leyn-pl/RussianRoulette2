# Russian Roulette 2 by LEYN

# Modules
# pip install rusrul_lib
# pip install colored
import random
import rusrul_lib as rrl
import ui
import text

buffer = ui.buffer()

# Global vars
run = True
gameover = False
ghost_hp = 60
player_hp = 60
rev = rrl.revolver()
acts = {
    'Ударить': 'punch()',
    'Выстрел во врага': 'shoot()',
    'Выстрел в себя': 'shoot(True)'
}
items = {
    'A': ['Патрон', 2, 'use_ammo()'],
    'B': ['Бинты', 1, 'heal()'],
    'C': ['Лёд', 0, 'use_ice()'],
    'D': ['Светошумовая', 0, 'use_flashbang()'],
    'E': ['Проклятие', 0, 'curse()'],
    'F': ['Дополнительный кубик', 0, 'extra_dice()']
}
event = ['game_start', 0, 'ghost']
dice = False
turn = False
midtext = []
game_over = False
ghost_turn = False
last_turn = ''
rev_damage = 1
effect = ''
effect_duration = 0
dice_result = []
dice_handle_id = -1
turnid = 0
prompt = ''
using_extra_dice = False
# Stat
bullets_ghost = 0
bullets_player = 0
items_used = 0

rev.strAmmo = '@'
rev.strEmpty = '.'

# Game over
def game_victory():
    global midtext
    midtext = text.victory + [
        '',
        f'ВЫ победили! Ходов: {(turnid+1)//2}',
        f'Пуль выстрелено в ПРИВИДЕНИЕ/ВАС: {bullets_ghost}/{bullets_player}',
        f'Предметов использовано: {items_used}'
    ]

def game_defeat():
    global midtext
    midtext = text.defeat + [
        '',
        f'ВЫ проиграли! Ходов: {(turnid+1)//2}',
        f'Пуль выстрелено в ПРИВИДЕНИЕ/ВАС: {bullets_ghost}/{bullets_player}',
        f'Предметов использовано: {items_used}'
    ]    

# Acts
def damage(amount, player=False):
    global ghost_hp, player_hp
    if player:
        player_hp -= amount*2
        if player_hp <= 0:
            player_hp = 0
            game_defeat()
    else:
        ghost_hp -= amount
        if ghost_hp <= 0:
            ghost_hp == 0
            game_victory()
def punch():
    global event, last_turn
    damage(2)
    event = ['punch', 0, 'ghost_hit']
    last_turn = 'attack'

def shoot(player=False):
    global rev, event, rev_damage, last_turn, bullets_ghost, bullets_player
    result = rev.shoot()
    if result and not player:
        damage(rev_damage)
        event = ['plr_shot', 0, 'ghost_shot']
        bullets_ghost += 1
    elif not result and not player:
        event = ['plr_miss', 0, 'ghost_happy']
    elif result and player:
        damage(rev_damage, True)
        event = ['plr_suicide', 0, 'ghost_question']
        bullets_player += 1
    elif not result and player:
        event = ['plr_suicide_miss', 0, 'ghost_bored']
    rev_damage += result
    last_turn = 'suicide' if player else 'attack'

def ghost_shoot(player=True):
    global rev, event, rev_damage, bullets_ghost, bullets_player
    result = rev.shoot()
    if result and not player:
        damage(rev_damage)
        event = ['gh_suicide_hit', 0, 'ghost_shot']
        bullets_ghost += 1
    elif not result and not player:
        event = ['gh_suicide_miss', 0, 'ghost_happy']
    elif result and player:
        damage(rev_damage, True)
        event = ['gh_attack_hit', 0, 'ghost_happy']
        bullets_player += 1
    elif not result and player:
        event = ['gh_attack_miss', 0, 'ghost_bored']
    rev_damage += result

def throw_dice(amount):
    global dice_result
    dice_result = [random.randint(1, 6) for _ in range(amount)]

def ghost_heal():
    global event
    if ghost_hp < 56 and effect != 'CURSED':
        damage(-4)
        event = ['gh_heal', 0, 'ghost_happy']
    else:
        event = ['gh_heal_fail', 0, 'ghost_bored']

# Items
def use_ammo(slot=None) -> bool:
    global prompt, rev, event, items, items_used
    if not slot:
        if rev.ammoCount() == 6:
            event = ['reload_fail', 0, 'ghost_question']
            items['A'][1] += 1
            return True
        prompt = f'КУДА ЗАРЯДИТЬ ПАТРОН? ({rev}) (1-6)'
    else:
        if not inp.isdigit: return
        if inp not in '123456': return        
        slot = int(slot) - 1
        rev.strAmmo, rev.strEmpty = '1', '0'
        new_clip = str(rev)[:slot] + '1' + str(rev)[slot+1:]
        if str(rev) != new_clip:
            rev.load(new_clip)
            prompt = ''
            rev.spin()
            event = ['reload', 0, 'ghost_bored']
            rev.strAmmo, rev.strEmpty = '@', '.'
            items_used += 1
            return True
        rev.strAmmo, rev.strEmpty = '@', '.'

def heal():
    global event, turn, items_used
    if player_hp <= 56:
        damage(-2, True)
        event = ['heal', 0, 'ghost_question']
        turn = False
        items_used += 1
    else:
        event = ['heal_fail', 0, 'ghost_bored']
def use_ice():
    global rev_damage, turn, event, items_used
    rev_damage = 1
    if rev_damage < 10:
        event = ['ice', 0, 'ghost_question']
    else:
        event = ['ice', 0, 'ghost_bored']
    turn = False
    items_used += 1

def use_flashbang():
    global effect, effect_duration, turn, event, items_used
    effect = 'STUNNED'
    effect_duration = 2
    event = ['flashbang', 0, 'ghost_stunned']
    turn = False
    items_used += 1

def curse():
    global effect, effect_duration, turn, event, items_used
    effect = 'CURSED'
    effect_duration = 3
    event = ['curse', 0, 'ghost_hit']
    turn = False
    items_used += 1

def extra_dice():
    global turn, event, dice, using_extra_dice, items_used
    throw_dice(1)
    event = ['extra_dice', 0, 'dice_1']
    turn = False
    dice = True
    using_extra_dice = True
    items_used += 1

# Game loop
while run:
    # Draw top UI
    ui.healthBar(buffer, "ПРИВИДЕНИЕ", ghost_hp)
    act_id = 1
    txt = ui.splitText(text.events[event[0]][event[1]])
    for act in acts:
        buffer.write(f' {act_id}. {act:<25}|' if not game_over else ' '*29+'|', True) # Action
        buffer.write(' '*30) # Separator
        buffer.write(f'| {txt[act_id - 1]:^58}' if not game_over else '|') # Text
        act_id += 1
    buffer.write(f'{"действие":-^29}' + '#' + ' '*30 + '#' + '-'*59, True)

    # Effect
    buffer.write(f'{effect + ": " + str(effect_duration):^120}' if effect else '', True)
    # Draw event
    for i in range(10):
        if midtext and game_over:
            buffer.write(f'{midtext[i]:^120}')
        else:
            frame_id = min(event[1], len(event[2])-1)
            buffer.write(f'{text.frames[event[2]][i]:^120}', True)            
    buffer.write('', True)
    if event[2] == 'peek':
        buffer.txt[10] = buffer.txt[10][:59] + str(rev)[0] + buffer.txt[10][60:]
    elif event[2] == 'dice_1':
        buffer.txt[12] = buffer.txt[12][:59] + str(dice_result[0]) + buffer.txt[12][60:]
    elif event[2] == 'dice_2':
        buffer.txt[12] = buffer.txt[12][:50] + str(dice_result[0]) + buffer.txt[12][51:]
        buffer.txt[14] = buffer.txt[14][:68] + str(dice_result[1]) + buffer.txt[14][69:]
    
    # Draw bottom UI
    buffer.write(f'{"урон: "+str(rev_damage):-^59}' + '#', True) # Revolver
    buffer.write(' '*30) # Separator
    buffer.write('#' + f'{"предметы":-^29}') # Items
    for i in range(6):
        buffer.write('' if turn else ui.Fore.dark_gray, True)
        buffer.write(f'{text.revolver[i]:>28}')
        if i == 1:
            for j in range(6):
                buffer.write('   /\\' if rev.ammoCount() > j else '     ')
        elif i == 2 or i == 3:
            for j in range(6):
                buffer.write('   ||' if rev.ammoCount() > j else '     ')
        elif i == 4:
            for j in range(6):
                buffer.write('   ||' if rev.ammoCount() > j else '   __')
        else:
            buffer.write(' '*30)
        buffer.write(ui.Style.reset + ' |') # Revolver
        buffer.write(' '*30) # Separator
        item_key = list(items.keys())[i]
        buffer.write(f'| {item_key+"." if not game_over else '  '} {items[item_key][0]:<20} x {items[item_key][1]}' if items[item_key][1] > 0 or item_key == 'A' else '|')
    ui.healthBar(buffer, "ВЫ", player_hp, True)

    buffer.flush()
    
    # Get input
    if prompt and not midtext:
        inp = input(f'{prompt} > ').upper()
    elif turn and not midtext:
        # Get input
        inp = input('ДЕЙСТВИЕ > ').upper()
    else:
        # Wait
        input('...')

    # Turn logic
    if event[1]+1 < len(text.events[event[0]]):
        event[1] += 1
    elif game_over:
        pass
    elif dice:
        # Dice logic
        if dice_handle_id < len(dice_result)-1:
            dice_handle_id += 1
            if dice_result[dice_handle_id] == 1:
                damage(1, True)
                event = ['dice_1', 0, f'dice_{len(dice_result)}']
                continue
            elif dice_result[dice_handle_id] == 2:
                items['A'][1] += 1 if items['A'][1] < 9 else 0
                event = ['dice_2', 0, f'dice_{len(dice_result)}']
                continue
            elif dice_result[dice_handle_id] in [3, 4]:
                random_item = random.choice(list('BCDEF'))
                items[random_item][1] += 1 if items[random_item][1] < 9 else 0
                event = ['dice_34', 0, f'dice_{len(dice_result)}']
                continue
            elif dice_result[dice_handle_id] == 5:
                event = ['dice_5', 0, 'peek']
                continue
            else:
                damage(1)
                event = ['dice_6', 0, 'ghost_hit']
                continue
        if sum(dice_result) / 2 in dice_result:
            event = ['double', 0, 'dice_2']
            throw_dice(2)
            dice_handle_id  = -1
            continue
        event = ['turn', 0, 'ghost'] if not using_extra_dice else ['ghost_turn', 0, 'ghost']
        dice = False
        turn = not using_extra_dice
        ghost_turn = using_extra_dice
        turnid += using_extra_dice
        using_extra_dice = False
        dice_result = []
        dice_handle_id  = -1
    # Selecting action
    elif turn:
        event = ['turn', 0, 'ghost']
        if prompt:
            if prompt[:4] == 'КУДА': # Insetring ammo
                if use_ammo(inp): turn = False
        else:
            if inp.isdigit(): # Act
                inp = int(inp) - 1
                if inp in range(3):
                    exec(acts[list(acts.keys())[inp]])
                    turn = False
            elif inp in list('ABCDEF'):
                if items[inp][1] > 0:
                    exec(items[inp][2])
                    items[inp][1] -= 1
    elif ghost_turn:
        # Tick effect
        if effect_duration > 0:
            effect_duration -= 1
        else:
            effect = ''
        # Ghost action
        if effect == 'STUNNED':
            event = ['gh_stunned', 0, 'ghost_stunned']
            ghost_turn = False
        elif rev.ammoCount() == 0:
            rev.load('001100')
            rev.spin()
            event = ['gh_reload', 0, 'ghost_bored']
        else:
            if last_turn == 'attack':
                ghost_shoot()
            elif last_turn == 'suicide':
                ghost_shoot(False)
            else:
                ghost_heal()
            ghost_turn = False
    elif not dice:
        if midtext:
            game_over = True
        else:
            turnid += 1
            if turnid % 2 == 1:
                last_turn = ''
                if effect == 'STUNNED':
                    turn = True
                    event = ['turn', 0, 'ghost_stunned']                
                elif effect == 'CURSED':
                    dice = True
                    throw_dice(1)
                    event = ['dice_cursed', 0, 'dice_1']
                else:
                    dice = True
                    throw_dice(2)
                    event = ['dice', 0, 'dice_2']
            else:
                ghost_turn = True
                event = ['ghost_turn', 0, 'ghost']