from .completer import filter_by_title
from .completer import filter_by_name
import os


def note_completer(env, params):
    if env.working_directory == '/Tags':
        return [], 0
    elif env.working_directory == '/All Notes' or env.working_directory == '/':
        return filter_by_title(params, env.data_access.list_all_notes()), -len(params)
    elif env.working_directory.startswith('/Tags/'):
        tag_name = env.working_directory.split('/', 2)[-1]
        tag = env.data_access.get_tag_by_name(tag_name)
        return filter_by_title(params, tag.note), -len(params)
    else:
        notebook_name = env.working_directory.split('/')[-1]
        notebook = env.data_access.get_notebook_by_name(notebook_name)
        return filter_by_title(params, notebook.note), -len(params)


def lntag_completer(env, params):
    split = params.split(' |~ ')
    if len(split) == 1:
        return note_completer(env, params)
    elif len(split) == 2:
        tag_name = split[1].strip()
        return filter_by_name(tag_name, env.data_access.list_tags()), -len(tag_name)


def ulntag_completer(env, params):
    split = params.split(' |~ ')
    if len(split) == 1:
        return note_completer(env, params)
    elif len(split) == 2:
        note_title = split[0].strip()
        tag_name = split[1].strip()
        if env.data_access.has_note(note_title):
            note = env.data_access.get_note_by_title(note_title)
            return filter_by_name(tag_name, note.tag), -len(tag_name)
        else:
            return [], 0


def mv_completer(env, params):
    split = params.split(' |~ ')
    if len(split) == 1:
        return note_completer(env, params)
    elif len(split) == 2:
        notebook_name = split[1].strip()
        return filter_by_name(notebook_name, env.data_access.list_notebooks()), -len(notebook_name)


def addnote_processor(env, params):
    if env.working_directory == '/' or env.working_directory.startswith('/Tags') or env.working_directory == '/All Notes':
        print('You can add note when only you are in a notebook')
    else:
        title = params.strip()
        if not env.data_access.has_note(title):
            file_name = 'text_mode/temp/' + title + '.md'
            file = open(file_name, 'w')
            file.close()
            os.system(env.configuration.editor + ' "' + file_name + '"')
            file = open(file_name, 'r').read()
            notebook_name = env.working_directory.split('/')[-1]
            notebook = env.data_access.get_notebook_by_name(notebook_name)
            env.data_access.add_note(title, file, notebook)
            os.remove(file_name)
        else:
            print("There's already the note exist")
    return env


def edit_processor(env, params):
    title = params.strip()
    if env.data_access.has_note(title):
        note = env.data_access.get_note_by_title(title)
        file_name = 'text_mode/temp/' + title + '.md'
        file = open(file_name, 'w')
        file.write(note.content)
        file.close()
        os.system(env.configuration.editor + ' "' + file_name + '"')
        file = open(file_name, 'r').read()
        note.content = file
        env.data_access.save_note(note)
        os.remove(file_name)
    else:
        print("The note", title, 'is not found')
    return env


def rmnote_processor(env, params):
    title = params.strip()

    if env.data_access.has_note(title):
        check = input("Are you sure you want to delete this note?(y/n):")
        if check == 'y':
            note = env.data_access.get_note_by_title(title)
            env.data_access.delete_note(note)
            print('Delete success')
        else:
            print("Ok, we didn't delete it")
    else:
        print('No note named', title)

    return env


def rnnote_processor(env, params):
    split = params.split(' |~ ')
    if len(split) == 2:
        old_title = split[0].strip()
        new_title = split[1].strip()

        if env.data_access.has_note(new_title):
            print("There's already a note named", new_title)
        elif not env.data_access.has_note(old_title):
            print("There's no note named", old_title)
        else:
            note = env.data_access.get_note_by_title(old_title)
            note.title = new_title
            env.data_access.save_note(note)
    else:
        print('rnnote new_name |~ old_name')
    return env


def lntag_processor(env, params):
    split = params.split(' |~ ')
    if len(split) == 2:
        note_title = split[0].strip()
        tag_name = split[1].strip()

        if not env.data_access.has_note(note_title):
            print("There's no note named", note_title)
        elif not env.data_access.has_tag(tag_name):
            print("There's no tag named", tag_name)
        else:
            note = env.data_access.get_note_by_title(note_title)
            tag = env.data_access.get_tag_by_name(tag_name)
            env.data_access.link_note_with_tag(note, tag)
    else:
        print('lntag note_name |~ tag_name')
    return env


def ulntag_processor(env, params):
    split = params.split(' |~ ')
    if len(split) == 2:
        note_title = split[0].strip()
        tag_name = split[1].strip()

        if env.data_access.has_note(note_title):
            note = env.data_access.get_note_by_title(note_title)
            if env.data_access.has_tag(tag_name):
                tag = env.data_access.get_tag_by_name(tag_name)
                if tag in note.tag:
                    env.data_access.unlink_note_with_tag(note, tag)
                else:
                    print(note_title, "has'nt the tag", tag_name)
        else:
            print("There's no note named", note_title)
    else:
        print('ulntag note_name |~ tag_name')
    return env


def mv_processor(env, params):
    split = params.split(' |~ ')
    if len(split) == 2:
        note_title = split[0].strip()
        notebook_name = split[1].strip()

        if env.data_access.has_note(note_title):
            if env.data_access.has_notebook(notebook_name):
                note = env.data_access.get_note_by_title(note_title)
                notebook = env.data_access.get_notebook_by_name(notebook_name)
                env.data_access.move_note_to_notebook(note, notebook)
            else:
                print("There's no notebook named", notebook_name)
        else:
            print("There's no note named", note_title)
    else:
        print('mv note_name |~ notebook_name')
    return env
