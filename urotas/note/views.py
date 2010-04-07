#-*-coding=utf-8-*-
import simplejson

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.shortcuts import (render_to_response, get_list_or_404,
                              get_object_or_404)

from models import Note, Tag
from forms import (ModifyNoteForm, NewNoteForm, 
                   QueryNotesByTimeForm, SearchNoteForm)

@login_required
def index(request):
    notes = request.user.notes.all()[:17]
    return render_to_response('note/index.html',
                              {'notes':notes},
                              context_instance=RequestContext(request))

@login_required
def create(request):
    # DONE 将Note转换成合适的JSON对象(为了在前端上与下一任务保持一致,
    #      虽然只有一项, 也将结果放入列表中再返回)
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
            # TODO 异常情况, 加LOG
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
    # DONE 用django.form 实现 since, delta参数的获取
    # DONE 解决前端动态添加的note记录没有timestamp属性的问题
    form = QueryNotesByTimeForm(request.GET)
    if form.is_valid():
        notes = form.fetch_notes(request.user.notes)
        notes = [note.get_serializable() for note in notes]
        return HttpResponse(simplejson.dumps(notes),
                            mimetype='application/json')
    else:
        # TODO 处理出现异常参数的情况
        return HttpResponse('false',
                            mimetype='application/json')

@login_required
def search(request):
    form = SearchNoteForm(request.GET)
    if form.is_valid():
        tag_name = form.cleaned_data['tag']
        notes = request.user.notes.filter(
                        tags__content=tag_name).all()[:17]
        return render_to_response('note/search.html', {'notes':notes})
    else:
        # TODO 处理出现异常参数的情况
        return HttpResponse('false',
                            mimetype='application/json')
