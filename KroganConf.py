from Parameter import *

#TODO add weapons to config. requires manual change

FortificationEffect = Effect(2, 0, 2, 0)

def cooldown(value: int):
    return ParameterConf(value, 0, value, -1, [FortificationEffect])

config = {
        'Heal': ('HP', ParameterConf(50, -100, 50, 5), []),
        'Shields': ('Shield', ParameterConf(35, 0, 35, 3), []),
\
        'Carnage': ('Combat cooldown', cooldown(4), []),
        'Conc shot': ('Combat cooldown', cooldown(3), []),
        'Fortification': ('Combat cooldown', cooldown(4), [FortificationEffect]),
        'Fortification melee boost': ('Fortification melee boost', cooldown(4), []),
\
        'Pull': ('Biotic cooldown', cooldown(3), []),
        'Warp': ('Biotic cooldown', cooldown(2), []),
\
        'Shield boost': ('Shield boost cooldown', cooldown(10), []),
        'First aid': ('First aid cooldown', cooldown(10), []),
}


holder = ParameterHolder()
holder_config = HolderConfig(holder, config)
holder_config.action('Heal')

