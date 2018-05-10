from text_mode.init import init
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from .command_completer import CommandCompleter


def main():
    env = init()

    while True:
        try:
            user_input = prompt(env.working_directory + '>', history=FileHistory('text_mode/temp/history'),
                    auto_suggest=AutoSuggestFromHistory(),
                    completer=CommandCompleter(env)).strip()
            if len(user_input) != 0:
                command = user_input.split(' ', 1)[0]
                if user_input == 'quit':
                    break
                elif command in env.cmd_processors.keys():
                    if len(user_input.split(' ', 1)) == 1:
                        params = ''
                    else:
                        params = user_input.split(' ', 1)[1]
                    env = env.cmd_processors[command](env, params)
                else:
                    print('Unknown command')

        except EOFError:
            break
