from prompt_toolkit.completion import Completer, Completion


class CommandCompleter(Completer):
    def __init__(self, env):
        self.env = env

    def get_completions(self, document, complete_event):
        line = document.current_line_before_cursor.strip()

        if len(line.split(' ', 1)) < 2 and not document.current_line_before_cursor.endswith(' '):
            for command in self.env.cmd_processors.keys():
                if command.startswith(document.get_word_before_cursor()):
                    yield Completion(command, start_position=-len(line))

        else:
            command = line.split(' ', 1)[0]
            if len(line.split(' ', 1)) == 1:
                params = ''
            else:
                params = line.split(' ', 1)[1]
            if command in self.env.cmd_completers.keys():
                completer_list, start_position = self.env.cmd_completers[command](self.env, params)
                for item in completer_list:
                    yield Completion(item, start_position=start_position)
