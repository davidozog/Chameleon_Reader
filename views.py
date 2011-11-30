from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.views.generic.list_detail import object_list
from django.core.files import File
from Chameleon_Reader import settings

from notes.models import Notes
from contents.models import Article, Node, Achievement, Book
from gameprofile.models import UserProfile

from contents.views import AccountForm

from xml.etree import ElementTree
import urllib2
import subprocess
import os

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
            ft2_book = book_list.filter(name="Team Fortress 2")[0]
            wow_book = book_list.filter(name="World of Warcraft")[0]
            return render_to_response('library/library.html', {'book_list':book_list, 'user':USER, 'ft2_book':ft2_book, 'wow_book':wow_book})
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
    gameprofile = UserProfile.objects.get(user=USER)
    ach_message = ''
    avatar_img = ''
    try:
        user_ach = gameprofile.achievements.all()
        #if len(user_ach) == 0:
        #  ach_message = 'You don\'t have any achievements.'
    except:
        user_ach = []
        ach_message = 'You don\'t have any achievements.'

    if gameprofile.steamid:
        steamID = gameprofile.steamid
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
            avatar_S = tree.find("avatarIcon").text
            avatar_M = tree.find("avatarMedium").text
            avatar_L = tree.find("avatarFull").text
            spS = subprocess.call('wget ' + avatar_S + ' -O ' + settings.PREFIX + '/static/img/avatars/' + USER.username + '_S.jpg', shell=True)
            spM = subprocess.call('wget ' + avatar_M + ' -O ' + settings.PREFIX + '/static/img/avatars/' + USER.username + '_M.jpg', shell=True)
            spL = subprocess.call('wget ' + avatar_L + ' -O ' + settings.PREFIX + '/static/img/avatars/' + USER.username + '_L.jpg', shell=True)

            print 'TESTING'

            av_L_path = settings.PREFIX + '/static/img/avatars/' + USER.username + '_L.jpg'
            av_M_path = settings.PREFIX + '/static/img/avatars/' + USER.username + '_M.jpg'
            av_S_path = settings.PREFIX + '/static/img/avatars/' + USER.username + '_S.jpg'
            av_L_file = open(av_L_path)
            av_M_file = open(av_M_path)
            av_S_file = open(av_S_path)
            avLf = File(av_L_file)
            avMf = File(av_M_file)
            avSf = File(av_S_file)

            # Get achievements
            data = urllib2.urlopen(
                "http://steamcommunity.com/profiles/%s/stats/%s/?xml=1" %
                (steam64ID, "TF2"))
            tree = ElementTree.parse(data)

            achievements = []
            iconClosed = {}
            iconOpen = {}
            for achievement in tree.getroot().find("achievements").findall(
                "achievement"):
                if not achievement.find("unlockTimestamp") == None:
                    achievements.append(achievement.find("name").text)
                    iconClosed[achievement.find("name").text] = achievement.find("iconClosed").text
                    iconOpen[achievement.find("name").text] = achievement.find("iconOpen").text

            _age = form.cleaned_data['age']
            _language = form.cleaned_data['language']
            to_remove = UserProfile.objects.filter(user=USER)
            to_remove.delete()
            updated_prof = UserProfile(user=USER, age=_age, language=_language, steamid=steamID,
                                       avatar_large = avLf, avatar_medium = avMf, avatar_small = avSf)

            updated_prof.save()

            for achie in achievements:
                achiModel = Achievement.objects.get(name=achie)
                # This code was used to gather all the Achievement Icon images
                #ach_IC_path = os.getcwd() + '/static/img/achievements/' + achiModel.name.replace(' ', '_').replace('\'','_').replace('(', '').replace(')', '') + '_closed.jpg'
                #ach_IO_path = os.getcwd() + '/static/img/achievements/' + achiModel.name.replace(' ', '_').replace('\'','_').replace('(', '').replace(')', '') + '_open.jpg'
                #ach_IC = subprocess.call('wget ' + iconClosed[achiModel.name] + ' -O ' + ach_IC_path, shell=True)
                #ach_IO = subprocess.call('wget ' + iconOpen[achiModel.name] + ' -O ' + ach_IO_path, shell=True)
                #ach_IC_file = open(ach_IC_path)
                #ach_IO_file = open(ach_IO_path)
                #ach_IC_f = File(ach_IC_file)
                #ach_IO_f = File(ach_IO_file)
                
                #achiModel.icon_closed = ach_IC_f
                #achiModel.icon_open = ach_IO_f
                #achiModel.save()

                updated_prof.achievements.add(achiModel)
                
            updated_prof.save()
            
            avatar_img = updated_prof.avatar_large.name
            achievements = updated_prof.achievements.all()

        else:
            achievements = []
            _age = ''
            _language = ''
            ach_message = 'None'

        return render_to_response('templates/account_settings.html', {'user':USER, 'username':USER.username, 'achievements':achievements, 'ach_message':ach_message, 'steamID':steamID, 'age':_age, 'language':_language, 'form':form, 'avatar_img':avatar_img }, context_instance=RequestContext(request))

    else:
        if steamID:
            age = gameprofile.age
            language = gameprofile.language
            form = None
            avatar_img = gameprofile.avatar_large.name
        else:
            form = AccountForm()  # An unbound form
            age = ''
            language = ''
            ach_message = 'None'

        return render_to_response('templates/account_settings.html', {'user':USER, 'username':USER.username, 'achievements':user_ach, 'ach_message':ach_message, 'form':form, 'steamID':steamID, 'age':age, 'language':language, 'avatar_img':avatar_img }, context_instance=RequestContext(request))
