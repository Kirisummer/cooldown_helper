from Parameter import *
from Tui import *

#TODO add weapons to config. requires manual change

FortificationEffect = Effect(2, 0, 2, 0)

def cooldown(value: int, wait: int = 1):
    return ParameterConf(value, 0, value, -1, {FortificationEffect}, wait)

holder = ParameterHolder()
config = {
        'Heal': ConfigEntry('HP', ParameterConf(50, -100, 50, 5)),
        'Shields': ConfigEntry('Shield', ParameterConf(35, 0, 35, 3)),
\
        'Carnage': ConfigEntry('Combat', cooldown(4)),
        'Conc shot': ConfigEntry('Combat', cooldown(3)),
        'Fortification': ConfigEntry('Combat', cooldown(4), {FortificationEffect}),
        'FortificationBoost': ConfigEntry('FortificationBoost', ParameterConf(4, 0, 4, -1, 1), [], {FortificationEffect}),
\
        'Pull': ConfigEntry('Biotic', cooldown(3)),
        'Warp': ConfigEntry('Biotic', cooldown(2)),
\
        'ShieldBoost': ConfigEntry('ShieldBoost', cooldown(10, 2)),
        'FirstAid': ConfigEntry('FirstAid', cooldown(10)),
\
        'Shotgun': ConfigEntry('Shotgun', ParameterConf(3, 0, 3, 0)),
        'Rifle': ConfigEntry('Rifle', ParameterConf(30, 0, 30, 0)), #TODO change rifle ammo amount
        'Pistol': ConfigEntry('Pistol', ParameterConf(12, 0, 12, 0)), #TODO change pistol ammo amount
}

action_handler = ActionHandler(holder, config, ['Heal', 'Shields', 'Shotgun', 'Rifle', 'Pistol'])
tui = Tui(action_handler)
tui.run()
