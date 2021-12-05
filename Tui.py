class ActionHandler:
    LOCK_ACTIONS = '!lock', '!l'
    UNLOCK_ACTIONS = '!unlock', '!ul'
    NEXT_ACTIONS = '!next', '!n'
    CHANGE_ACTIONS = '!change', '!c'

    def __init__(self, holder, config, init_actions):
        self.holder = holder
        self.config = config

        for action in init_actions:
            self.action(action)

    def action(self, action: str, *args):
        if action in type(self).LOCK_ACTIONS:
            for pool in args:
                self.lock(pool, True)

        elif action in type(self).UNLOCK_ACTIONS:
            for pool in args:
                self.lock(pool, False)

        elif action in type(self).NEXT_ACTIONS:
            self.holder.next_action()

        elif action in type(self).CHANGE_ACTIONS:
            try:
                self.change(args[0], args[1])
            except IndexError:
                print('Not enough arguments')

        else:
            self.run_action(action)

    def lock(self, pool: str, is_locked: bool):
        try:
            self.holder.set_locked(pool, is_locked)
        except KeyError:
            print('No such pool: ' + pool)
            return

    def change(self, pool: str, value: str):
        is_delta = (value[0] == 'd')
        try:
            self.holder[pool]
        except KeyError:
            print('No such pool: ' + pool)
            return

        if is_delta:
            int_value = Number(value[1:])
            self.holder.apply_delta(pool, int_value)
        else:
            int_value = Number(value)
            self.holder.change_param(pool, int_value)

    def run_action(self, action: str):
        entry = self.config.get(action)
        if entry is None:
            print('No such action: ' + action)
            return

        self.holder[entry.pool_name] = entry.config
        for effect in entry.add_effects:
            self.holder.add_effect(effect)
        for effect in entry.remove_effects:
            self.holder.remove_effect(effect)


class Tui:
    def __init__(self, action_handler: ActionHandler):
        self.handler = action_handler

    def print_holder(self):
        print('{')
        for pool, lock in self.handler.holder.items():
            print('\t', pool, ':', lock.parameter)
        print('}')

    def run(self):
        self.print_holder()
        inp = input()
        while inp != 'exit':
            action, *args = inp.split()
            self.handler.action(action, *args)
            self.print_holder()
            inp = input()
