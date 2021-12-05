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
}

action_handler = ActionHandler(holder, config, ['Heal', 'Shields'])
tui = Tui(action_handler)
tui.run()
