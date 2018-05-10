from .ls import ls_processor
from .cd import cd_processor
from .notebook import addnb_processor, rmnb_processor, rnnb_processor
from .tag import addtag_processor, rmtag_processor, rntag_processor
from .note import addnote_processor, edit_processor, rmnote_processor, rnnote_processor
from .note import lntag_processor, ulntag_processor
from .note import mv_processor
from .help import help_processor

from .cd import cd_completer
from .notebook import notebook_completer
from .tag import tag_completer
from .note import note_completer
from .note import lntag_completer
from .note import ulntag_completer
from .note import mv_completer
from .help import help_completer


def prelude(env):
    env.cmd_descriptions += [
        ['ls [-f=xxx]', 'List all content in the current directory'],
        ['cd dirname', 'Step into a directory'],
        ['addnb name', 'Create a notebook'],
        ['rmnb name', 'Delete the notebook'],
        ['rnnb old_name |~ new_name', 'Rename the notebook'],
        ['addtag name', 'Create a tag'],
        ['rmtag name', 'Delete the tag'],
        ['rntag old_name |~ new_name', 'Rename the tag'],
        ['addnote title', 'Create a note'],
        ['edit title', 'Edit the note'],
        ['rmnote title', 'Delete the note'],
        ['rnnote old_title |~ new_title', 'Rename the note'],
        ['lntag note_name |~ tag_name', 'Link note with tag'],
        ['ulntag note_name |~ tag_name', 'Unlink note with tag'],
        ['mv note_name |~ notebook_name', 'Move the note to the notebook'],
        ['help', 'Show this helper'],
        ['quit', 'Quit Knowledge']
    ]

    env.cmd_processors['cd'] = cd_processor
    env.cmd_processors['ls'] = ls_processor
    env.cmd_processors['addnb'] = addnb_processor
    env.cmd_processors['rmnb'] = rmnb_processor
    env.cmd_processors['rnnb'] = rnnb_processor
    env.cmd_processors['addtag'] = addtag_processor
    env.cmd_processors['rmtag'] = rmtag_processor
    env.cmd_processors['rntag'] = rntag_processor
    env.cmd_processors['addnote'] = addnote_processor
    env.cmd_processors['edit'] = edit_processor
    env.cmd_processors['rmnote'] = rmnote_processor
    env.cmd_processors['rnnote'] = rnnote_processor
    env.cmd_processors['lntag'] = lntag_processor
    env.cmd_processors['ulntag'] = ulntag_processor
    env.cmd_processors['mv'] = mv_processor
    env.cmd_processors['help'] = help_processor
    env.cmd_processors['quit'] = None

    env.cmd_completers['cd'] = cd_completer
    env.cmd_completers['rmnb'] = notebook_completer
    env.cmd_completers['rnnb'] = notebook_completer
    env.cmd_completers['rmtag'] = tag_completer
    env.cmd_completers['rntag'] = tag_completer
    env.cmd_completers['edit'] = note_completer
    env.cmd_completers['rmnote'] = note_completer
    env.cmd_completers['rnnote'] = note_completer
    env.cmd_completers['lntag'] = lntag_completer
    env.cmd_completers['ulntag'] = ulntag_completer
    env.cmd_completers['mv'] = mv_completer
    env.cmd_completers['help'] = help_completer

    return env



