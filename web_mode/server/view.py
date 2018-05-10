from django.http import HttpResponse
from lib.database import engine
from lib.data_access import DataAccess
from markdown import markdown
from django.views.decorators.csrf import csrf_exempt
import json


data_access = DataAccess(engine)


def to_dict(obj):
    return list(map(lambda x: {
        'id': x.id,
        'name': x.name,
        'notes': list(map(lambda y: y.title, x.note))
    }, obj))


def list_notebooks(request):
    notebooks = data_access.list_notebooks()
    notebooks_json = to_dict(notebooks)
    return HttpResponse(json.dumps(notebooks_json))


def list_tags(request):
    tags = data_access.list_tags()
    tags_json = to_dict(tags)
    return HttpResponse(json.dumps(tags_json))


def get_note(request):
    note_title = request.GET.get('note_title')
    if data_access.has_note(note_title):
        note = data_access.get_note_by_title(note_title)
        note_json = {}
        note_json['id'] = note.id
        note_json['title'] = note.title
        note_json['content'] = note.content
        note_json['content_html'] = markdown(note.content,
                                extensions=['markdown.extensions.extra',
                                            'markdown.extensions.codehilite',
                                            'markdown.extensions.toc',
                                            'markdown.extensions.tables'])
        note_json['create_time'] = str(note.create_time)
        note_json['last_modified'] = str(note.last_modified)
        note_json['tag'] = [tag.name for tag in note.tag]
        return HttpResponse(json.dumps(note_json))
    else:
        return HttpResponse()


@csrf_exempt
def mv_note(request):
    req = json.loads(request.body)
    note_title = req['note_title']
    notebook_name = req['notebook_name']
    if data_access.has_note(note_title) and data_access.has_notebook(notebook_name):
        note = data_access.get_note_by_title(note_title)
        notebook = data_access.get_notebook_by_name(notebook_name)
        data_access.move_note_to_notebook(note, notebook)
    return HttpResponse()


def delete_note(request):
    return


def save_note(request):
    return
