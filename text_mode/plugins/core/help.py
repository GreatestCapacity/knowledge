from prettytable import PrettyTable


def help_processor(env, params):
    param = params.strip()
    if param == '':
        cmd_desc = PrettyTable(['Command', 'Description'])
        cmd_desc.padding_width = 1
        cmd_desc.align = 'l'
        for row in env.cmd_descriptions:
            cmd_desc.add_row(row)
        print(cmd_desc)
    elif param in env.cmd_details.keys():
        env.cmd_detail[param]()
    else:
        print('No details information about this command')
    return env


def help_completer(env, params):
    return list(filter(lambda x: x.startswith(params), env.cmd_details.keys())), -len(params)
