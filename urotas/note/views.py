#-*-coding=utf-8-*-
import simplejson

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.shortcuts import (render_to_response, get_list_or_404,
                              get_object_or_404)

from models import Note, Tag
from forms import ModifyNoteForm, NewNoteForm, QueryNoteForm

@login_required
def index(request):
    # TODO If there is only one page of notes, don't call 
    #      `loadOnScroll` at the frontend
    notes = request.user.notes.all()[:17]
    return render_to_response('note/index.html',
                              {'notes':notes},
                              context_instance=RequestContext(request))

@login_required
def create(request):
    # TODO Receive a `timestamp` parameter and return all the
    #      notes that is modified after `timestamp`. Because
    #      in rare cases uses open the same page multiple times
    #      , and if we just return the note just added we would
    #      miss some notes submitted in other pages.
    if request.method == 'POST':
        form = NewNoteForm(request.POST)
        if form.is_valid():
            note = Note(author=request.user,
                        content=form.cleaned_data['content'])
            note.save()

            data = [note.get_serializable()]
            return HttpResponse(simplejson.dumps(data),
                                mimetype='application/json')
    return HttpResponse('false', mimetype='application/json')

@login_required
def modify(request):
    if request.method == 'POST':
        form = ModifyNoteForm(request.user, request.POST)
        if form.is_valid():
            saved_note = form.save()
            notes_query = QueryNotesByTimeForm(request.POST)
            if notes_query.is_valid():
                notes = notes_query.fetch_notes(request.user.notes)
                notes = [note.get_serializable() for note in notes]
                return HttpResponse(simplejson.dumps(notes),
                                    mimetype='application/json')
            return HttpResponse('true', mimetype='application/json')
        else:
            # TODO add log info
            return HttpResponse('false', mimetype='application/json')

@login_required
def remove(request):
    if 'note_id' in request.REQUEST:
        note_id = request.REQUEST['note_id']
        note = Note.objects.get(id=note_id)
        note.delete()
        return HttpResponse('true', mimetype='application/json')


@login_required
def list(request, format="html"):
    note_query = QueryNoteForm(request.GET)
    if note_query.is_valid():
        notes = note_query.fetch_records(Note.objects)

        if format == 'json':
            notes = [note.get_serializable() for note in notes]
            return HttpResponse(simplejson.dumps(notes),
                                mimetype='application/json')
        elif format == 'html':
            # TODO Make the page remember what query is made.
            #      how to regenerate the query dict? 
            #      will request.GET be perfect for this?
            query = note_query.query_as_dict()
            return render_to_response('note/search.html',
                                      {'notes':notes, 'query': simplejson.dumps(query)},
                                      RequestContext(request))
    else:
        # TODO a proper way to handle invalid format?
        return HttpResponse('false',
                            mimetype='application/json')
