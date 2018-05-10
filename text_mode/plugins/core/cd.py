from .completer import filter_by_name


# Environment, str -> Environment
def cd_processor(env, params):
    name = params.strip()

    if name == '..':
        if env.working_directory == '/' and name == '..':
            print('You are in the root directory')
        elif name == '..':
            env.working_directory = '/' + ''.join(env.working_directory.split('/')[:-1])

    elif env.working_directory == '/' and env.data_access.has_notebook(name) or name == 'Tags' or name == 'All Notes':
            env.working_directory += name
    elif env.working_directory == '/Tags' and env.data_access.has_tag(name):
            env.working_directory += '/' + name
    else:
        print("There's no directory named", name)

    return env


# Environment, str -> [str], int
def cd_completer(env, params):
    if env.working_directory == '/':
        return list(filter(lambda x: x.startswith(params), ['All Notes', 'Tags'])) + \
               filter_by_name(params, env.data_access.list_notebooks()), -len(params)
    elif env.working_directory == '/Tags':
        return filter_by_name(params, env.data_access.list_tags()), -len(params)

    return [], 0
