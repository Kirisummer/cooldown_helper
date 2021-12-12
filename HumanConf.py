from Parameter import *
from Tui import *
from math import floor

LOCK = True
UNLOCK = False

def cooldown(value: int, wait: int = 1):
    return ParameterConf(value, 0, value, -1, UNLOCK, set(), wait)

def ammo(max_value: int):
    return ParameterConf(max_value, 0, max_value, int(max_value * 0.2), LOCK)

def shield(max_value: int):
    return ParameterConf(max_value, 0, max_value, str(max_value * 0.2), LOCK)

holder = ParameterHolder()
config = {
        'Heal': ConfigEntry('HP', ParameterConf(17, -100, 17, 0, LOCK)),
        'Shields': ConfigEntry('Shields', shield(10)),
        'Tech': ConfigEntry('TechPoints', ParameterConf(7, 0, 7, 1, LOCK)),
\
        'Assasination': ConfigEntry('Combat', cooldown(5)),
        'Inferno grenade': ConfigEntry('Combat', cooldown(0)),
\
        'Hacking': ConfigEntry('Tech', cooldown(4)),
        'Overload': ConfigEntry('Tech', cooldown(3)),
        'TacticalCloak': ConfigEntry('Tech', cooldown(3)),
\
        'Cloak': ConfigEntry('Cloak', ParameterConf(4, 0, 4, -1)),
        'GrenadeFire': ConfigEntry('GrenadeFire', ParameterConf(4, 0, 4, -1)),
        'FirstAid': ConfigEntry('FirstAid', cooldown(10)),
\
        'Sniper': ConfigEntry('Sniper', ParameterConf(10, 0, 10, -1)), # Cooldown
        'Rifle': ConfigEntry('Rifle', ammo(30)), #TODO change rifle ammo amount
        'Pistol': ConfigEntry('Pistol', ammo(15)), #TODO change pistol ammo amount
}

action_handler = ActionHandler(holder, config, ['Heal', 'Shields', 'Tech', 'Rifle', 'Pistol'])
tui = Tui(action_handler)
tui.run()
