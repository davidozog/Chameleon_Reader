from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail
from django.views.generic.create_update import create_object
from django.views.generic.create_update import update_object
from django.views.generic.create_update import delete_object
from django.core.urlresolvers import reverse

from models import Notes
from contents.models import Article, Node, Achievement
from gameprofile.models import UserProfile
from forms import PartialNotesForm

def notes_list(request):
    """Menampilkan semua notes yang ada"""
    username = request.user.username
    USER = request.user
    achieved_all = 'none'
    if USER is not None:
        if USER.is_active:
            #notes = Notes.objects.get(user = user)
            #if len(notes) > 0:
            #  show_note = notes[0]
            #else:
            #  n = Note(note='')
            #  show_note = n
            #for note in notes:
            #  if note.user == user:
            #    show_note = note
            demo_article = Article.objects.filter(title='Chapter I Getting Started')
            chap1_ach = demo_article[0].achievements.all()
            gameprofile = UserProfile.objects.filter(user=USER)
            ach_message = ''
            try:
                if len(gameprofile) != 0:
                    try:
                        user_ach = gameprofile[0].achievements
                        for ach in chap1_ach:
                            try:
                                if user_ach.all().filter(name=ach.name):
                                    achieved_all = 'True'
                                else:
                                    achieved_all = 'False'
                                    break
                            except: 
                                achieved_all = 'Error' 
                                break
                    except:
                        pass
                else:
                    user_ach = []
                    ach_message = 'You don\'t have any achievements'
            except:
                user_ach = []
                ach_message = 'You don\'t have any achievements'
    return object_list(request, 
        queryset=Notes.objects.filter(user=request.user),
        template_name='notes/list.html',
        template_object_name='note',
        extra_context={'user':USER, 'username':username, 'gameprofile':gameprofile, 'achieved_all':achieved_all, 'ach_message':ach_message}
    )
    
def notes_detail(request, id):
    """Melihat rincian dari salah satu note"""
    username = request.user.username
    USER = request.user
    achieved_all = 'none'
    if USER is not None:
        if USER.is_active:
            #notes = Notes.objects.get(user = user)
            #if len(notes) > 0:
            #  show_note = notes[0]
            #else:
            #  n = Note(note='')
            #  show_note = n
            #for note in notes:
            #  if note.user == user:
            #    show_note = note
            demo_article = Article.objects.filter(title='Chapter I Getting Started')
            chap1_ach = demo_article[0].achievements.all()
            gameprofile = UserProfile.objects.filter(user=USER)
            ach_message = ''
            try:
                if len(gameprofile) != 0:
                    try:
                        user_ach = gameprofile[0].achievements
                        for ach in chap1_ach:
                            try:
                                if user_ach.all().filter(name=ach.name):
                                    achieved_all = 'True'
                                else:
                                    achieved_all = 'False'
                                    break
                            except: 
                                achieved_all = 'Error' 
                                break
                    except:
                        pass
                else:
                    user_ach = []
                    ach_message = 'You don\'t have any achievements'
            except:
                user_ach = []
                ach_message = 'You don\'t have any achievements'
    return object_detail(request,
    #return object_list(request, 
        queryset=Notes.objects.all(),
        #queryset=Notes.objects.filter(user=request.user),
        template_name='notes/detail.html',
        #template_name='notes/list.html',
        object_id=id,
        template_object_name='note',
        extra_context={'user':USER, 'username':username, 'gameprofile':gameprofile, 'achieved_all':achieved_all, 'ach_message':ach_message}
    )
    
    
def notes_create(request):
    """Membuat sebuah note baru"""

    username = request.user.username
    USER = request.user
    achieved_all = 'none'
    if USER is not None:
        if USER.is_active:
            #notes = Notes.objects.get(user = user)
            #if len(notes) > 0:
            #  show_note = notes[0]
            #else:
            #  n = Note(note='')
            #  show_note = n
            #for note in notes:
            #  if note.user == user:
            #    show_note = note
            demo_article = Article.objects.filter(title='Chapter I Getting Started')
            chap1_ach = demo_article[0].achievements.all()
            gameprofile = UserProfile.objects.filter(user=USER)
            ach_message = ''
            try:
                if len(gameprofile) != 0:
                    try:
                        user_ach = gameprofile[0].achievements
                        for ach in chap1_ach:
                            try:
                                if user_ach.all().filter(name=ach.name):
                                    achieved_all = 'True'
                                else:
                                    achieved_all = 'False'
                                    break
                            except: 
                                achieved_all = 'Error' 
                                break
                    except:
                        pass
                else:
                    user_ach = []
                    ach_message = 'You don\'t have any achievements'
            except:
                user_ach = []
                ach_message = 'You don\'t have any achievements'
    blank_user_note = Notes(user=USER)
    return create_object(request,
    #return object_list(request, 
        #model=Notes,
        form_class=PartialNotesForm,
        my_instance=blank_user_note,
        #queryset=Notes.objects.filter(user=request.user),
        template_name='notes/create.html',
        #template_name='notes/list.html',
        #template_object_name='note',
        post_save_redirect=reverse("notes_list"),
        extra_context={'user':USER, 'username':username, 'gameprofile':gameprofile, 'achieved_all':achieved_all, 'ach_message':ach_message}
    )
    
def notes_update(request, id):
    """Update sebuah note"""

    username = request.user.username
    USER = request.user
    achieved_all = 'none'
    if USER is not None:
        if USER.is_active:
            #notes = Notes.objects.get(user = user)
            #if len(notes) > 0:
            #  show_note = notes[0]
            #else:
            #  n = Note(note='')
            #  show_note = n
            #for note in notes:
            #  if note.user == user:
            #    show_note = note
            demo_article = Article.objects.filter(title='Chapter I Getting Started')
            chap1_ach = demo_article[0].achievements.all()
            gameprofile = UserProfile.objects.filter(user=USER)
            ach_message = ''
            try:
                if len(gameprofile) != 0:
                    try:
                        user_ach = gameprofile[0].achievements
                        for ach in chap1_ach:
                            try:
                                if user_ach.all().filter(name=ach.name):
                                    achieved_all = 'True'
                                else:
                                    achieved_all = 'False'
                                    break
                            except: 
                                achieved_all = 'Error' 
                                break
                    except:
                        pass
                else:
                    user_ach = []
                    ach_message = 'You don\'t have any achievements'
            except:
                user_ach = []
                ach_message = 'You don\'t have any achievements'
    return update_object(request,
    #return object_list(request, 
        model=Notes,
        #queryset=Notes.objects.filter(user=request.user),
        template_name='notes/update.html',
        #template_name='notes/list.html',
        object_id=id,
        post_save_redirect=reverse("notes_list"),
        extra_context={'user':USER, 'username':username, 'gameprofile':gameprofile, 'achieved_all':achieved_all, 'ach_message':ach_message}
    )
    
def notes_delete(request, id):
    """Hapus sebuah note"""
    username = request.user.username
    USER = request.user
    achieved_all = 'none'
    if USER is not None:
        if USER.is_active:
            #notes = Notes.objects.get(user = user)
            #if len(notes) > 0:
            #  show_note = notes[0]
            #else:
            #  n = Note(note='')
            #  show_note = n
            #for note in notes:
            #  if note.user == user:
            #    show_note = note
            demo_article = Article.objects.filter(title='Chapter I Getting Started')
            chap1_ach = demo_article[0].achievements.all()
            gameprofile = UserProfile.objects.filter(user=USER)
            ach_message = ''
            try:
                if len(gameprofile) != 0:
                    try:
                        user_ach = gameprofile[0].achievements
                        for ach in chap1_ach:
                            try:
                                if user_ach.all().filter(name=ach.name):
                                    achieved_all = 'True'
                                else:
                                    achieved_all = 'False'
                                    break
                            except: 
                                achieved_all = 'Error' 
                                break
                    except:
                        pass
                else:
                    user_ach = []
                    ach_message = 'You don\'t have any achievements'
            except:
                user_ach = []
                ach_message = 'You don\'t have any achievements'
    return delete_object(request,
        model=Notes,
        object_id=id,
        template_name='notes/delete.html',
        template_object_name='note',
        post_delete_redirect=reverse("notes_list"),
        extra_context={'user':USER, 'username':username, 'gameprofile':gameprofile, 'achieved_all':achieved_all, 'ach_message':ach_message}
    )
