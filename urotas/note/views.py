#-*-coding=utf-8-*-
import simplejson

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.shortcuts import (render_to_response, get_list_or_404,
                              get_object_or_404)

from models import Note, Tag
from forms import NoteForm

@login_required
def index(request):
    notes = request.user.notes.all()
    return render_to_response('note/index.html', {'notes':notes})

@login_required
def create(request):
    # DONE 将Note转换成合适的JSON对象(为了在前端上与下一任务保持一致,
    #      虽然只有一项, 也将结果放入列表中再返回)
    # TODO 从前端接收一个时间参数, 用于指明需要返回的对象起始于什么时间
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = Note(author=request.user,
                        content=form.cleaned_data['content'])
            note.save()

            data = [note.get_serializable()]
            return HttpResponse(simplejson.dumps(data),
                                mimetype='application/json')
    return HttpResponse('false', mimetype='application/json')

@login_required
def remove(request):
    if 'note_id' in request.REQUEST:
        note_id = request.REQUEST['note_id']
        note = Note.objects.get(id=note_id)
        note.delete()
        return HttpResponse('true', mimetype='application/json')

@login_required
def list(request):
    idx = request.GET.get('idx', 0)
    delta = request.GET.get('delta', 10)
    notes = request.user.notes.all()[idx:idx+delta]
    notes = [note.get_serializable() for note in notes]
    return HttpResponse(simplejson.dumps(notes),
                        mimetype='application/json')

"""
def list(request):
    content = request.GET['tag']
    tag = get_object_or_404(Tag, content=content)
    notes = tag.notes.all()
    return render_to_response('note/list.html', locals(), 
                              context_instance=RequestContext(request))
"""
