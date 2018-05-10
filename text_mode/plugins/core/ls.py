from prettytable import PrettyTable


# Environment, str -> Environment
def ls_processor(env, params):
    if env.working_directory == '/':
        notebooks = PrettyTable(['id', 'name'])
        notebooks.padding = 1
        notebooks.align = 'l'
        notebooks.add_row(['*', 'All Notes'])
        notebooks.add_row(['*', 'Tags'])
        for notebook in env.data_access.list_notebooks():
            notebooks.add_row([notebook.id, notebook.name])
        print(notebooks)

    elif env.working_directory == '/All Notes':
        notes = PrettyTable(['Title', 'Notebook', 'Create Time', 'Last Modified'])
        notes.padding = 1
        notes.align = 'l'
        for note in env.data_access.list_all_notes():
            notes.add_row([note.title, note.notebook.name, note.create_time, note.last_modified])
        print(notes)

    elif env.working_directory == '/Tags':
        tags = PrettyTable(['id', 'name'])
        tags.padding = 1
        tags.align = 'l'
        for tag in env.data_access.list_tags():
            tags.add_row([tag.id, tag.name])
        print(tags)

    elif env.working_directory.startswith('/Tags/'):
        tag_name = env.working_directory.split('/', 2)[-1]
        tag = env.data_access.get_tag_by_name(tag_name)
        notes = PrettyTable(['Title', 'Notebook', 'Create Time', 'Last Modified'])
        notes.padding = 1
        notes.align = 'l'
        for note in tag.note:
            notes.add_row([note.title, note.notebook.name, note.create_time, note.last_modified])
        print(notes)

    else:
        notebook_name = env.working_directory.split('/', 1)[-1]
        notebook = env.data_access.get_notebook_by_name(notebook_name)
        print(notebook_name)
        notes = PrettyTable(['Title',  'Tags', 'Create Time', 'Last Modified'])
        notes.padding = 1
        notes.align = 'l'
        for note in notebook.note:
            tag_names = ",".join(list(map(lambda x: x.name, note.tag)))
            notes.add_row([note.title, tag_names, note.create_time, note.last_modified])
        print(notes)
    return env
