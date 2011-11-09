from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.views.generic.list_detail import object_list

from notes.models import Notes
from contents.models import Article, Node, Achievement, Book
from gameprofile.models import UserProfile


def home(request, user=None):
    return render_to_response('templates/DAGuide.html')

def load_profile(request):
    username = request.POST['username']
    password = request.POST['password']
    USER = authenticate(username=username, password=password)
    if USER is not None:
        if USER.is_active:
            login(request, USER)
            book_list = Book.objects.all()
            return render_to_response('library/library.html', {'book_list': book_list, 'user':USER})
        else:
          return render_to_response('templates/login_error.html')
    else:
      return render_to_response('templates/login_error.html')

def load_book(request):
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
                queryset=Notes.objects.filter(user=USER),
                template_name='notes/list.html',
                template_object_name='note',
                extra_context={'user':USER, 'username':username, 'gameprofile':gameprofile, 'achieved_all':achieved_all, 'ach_message':ach_message}
            )
            #return render_to_response('templates/DAGuide.html', { 'user': user, 'username':username , 'note':show_note.note})
        else:
            return render_to_response('templates/account_not_active.html')
    else:
        return render_to_response('registration/login.html')
