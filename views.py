from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.views.generic.list_detail import object_list

from notes.models import Notes
from contents.models import Article, Node, Achievement, Book
from gameprofile.models import UserProfile

from contents.views import AccountForm

from xml.etree import ElementTree
import urllib2

def home(request, user=None):
    return render_to_response('templates/DAGuide.html')

def load_profile(request):
    username = request.POST['username']
    password = request.POST['password']
    USER = authenticate(username=username, password=password)
    if USER is not None:
        if USER.is_active:
            # See if user has a gameprofile; it not, create it
            try:
                gameprofile = UserProfile.objects.filter(user=USER)
                print gameprofile[0]
            except:
                prof = UserProfile(user=USER, age=25, language="", steamid="")
                prof.save()


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

def load_account(request):
    USER = request.user
    gameprofile = UserProfile.objects.filter(user=USER)
    ach_message = ''
    try:
        user_ach = gameprofile[0].achievements.all()
        ach_message = ''
    except:
        user_ach = []
        ach_message = 'You don\'t have any achievements'

    if gameprofile[0].steamid:
        steamID = gameprofile[0].steamid
    else:
        steamID = ''
    

    if request.method == 'POST':  # If the form has been submitted...
        form = AccountForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Get steam64ID
            steamID = form.cleaned_data['steamID']
 
            data = urllib2.urlopen("http://steamcommunity.com/id/%s?xml=1" % steamID)
            tree = ElementTree.parse(data)
            steam64ID = tree.find("steamID64").text

            # Get achievements
            data = urllib2.urlopen(
                "http://steamcommunity.com/profiles/%s/stats/%s/?xml=1" %
                (steam64ID, "TF2"))
            tree = ElementTree.parse(data)

            achievements = []
            for achievement in tree.getroot().find("achievements").findall(
                "achievement"):
                if not achievement.find("unlockTimestamp") == None:
                    achievements.append(achievement.find("name").text)

            _age = form.cleaned_data['age']
            _language = form.cleaned_data['language']
            to_remove = UserProfile.objects.filter(user=USER)
            to_remove.delete()
            # TODO: Add all user achievements to the database:
            updated_prof = UserProfile(user=USER, age=_age, language=_language, steamid=steamID)

            updated_prof.save()

            for achie in achievements:
                achiModel = Achievement.objects.filter(name=achie)[0]
                updated_prof.achievements.add(achiModel)
                
            updated_prof.save()
            
            #print achievements
            #return HttpResponseRedirect('/book/display_achievements')  # Redirect after POST
        else:
            achievements = []
            _age = ''
            _language = ''

        return render_to_response('templates/account_settings.html', {'user':USER, 'username':USER.username, 'achievements':achievements, 'ach_message':ach_message, 'steamID':steamID, 'age':_age, 'language':_language, 'form':form }, context_instance=RequestContext(request))

    else:
        if steamID:
            age = gameprofile[0].age
            language = gameprofile[0].language
            form = None
        else:
            form = AccountForm()  # An unbound form
            age = ''
            language = ''

        return render_to_response('templates/account_settings.html', {'user':USER, 'username':USER.username, 'achievements':user_ach, 'ach_message':ach_message, 'form':form, 'steamID':steamID, 'age':age, 'language':language }, context_instance=RequestContext(request))
