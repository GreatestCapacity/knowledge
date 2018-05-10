from .completer import filter_by_name


def notebook_completer(env, params):
    return filter_by_name(params, env.data_access.list_notebooks()), -len(params)


def addnb_processor(env, params):
    name = params.strip()

    env.data_access.add_notebook(name)

    return env


def rmnb_processor(env, params):
    name = params.strip()

    if env.data_access.has_notebook(name):
        check = input("Are you sure you want to delete this notebook and it's all notes?(y/n):")
        if check == 'y':
            notebook = env.data_access.get_notebook_by_name(name)
            env.data_access.delete_notebook(notebook)
            print('Delete success')
        else:
            print("Ok, we didn't delete it")
    else:
        print('No notebook named', name)

    return env


def rnnb_processor(env, params):
    split = params.split(' |~ ')
    if len(split) == 2:
        old_name = split[0].strip()
        new_name = split[1].strip()
        if env.data_access.has_notebook(new_name):
            print("There's already a notebook named", new_name)
        elif not env.data_access.has_notebook(old_name):
            print("There's no notebook named", old_name)
        else:
            notebook = env.data_access.get_notebook_by_name(old_name)
            notebook.name = new_name
            env.data_access.save_notebook(notebook)
    else:
        print('rnnb new_name |~ old_name')
    return env
