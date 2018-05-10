from .completer import filter_by_name


def tag_completer(env, params):
    return filter_by_name(params, env.data_access.list_tags()), -len(params)


def addtag_processor(env, params):
    name = params.strip()

    env.data_access.add_tag(name)

    return env


def rmtag_processor(env, params):
    name = params.strip()

    if env.data_access.has_tag(name):
        check = input("Are you sure you want to delete this tag?(y/n):")
        if check == 'y':
            tag = env.data_access.get_tag_by_name(name)
            env.data_access.delete_tag(tag)
            print('Delete success')
        else:
            print("Ok, we didn't delete it")
    else:
        print('No tag named', name)

    return env


def rntag_processor(env, params):
    split = params.split(' |~ ')
    if len(split) == 2:
        old_name = split[0].strip()
        new_name = split[1].strip()
        if env.data_access.has_tag(new_name):
            print("There's already a tag named", new_name)
        elif not env.data_access.has_tag(old_name):
            print("There's no tag named", old_name)
        else:
            tag = env.data_access.get_tag_by_name(old_name)
            tag.name = new_name
            env.data_access.save_tag(tag)
    else:
        print('rntag new_name |~ old_name')
    return env
