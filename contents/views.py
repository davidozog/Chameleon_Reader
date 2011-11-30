# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django import forms
from models import Article, Node, Book, Achievement
from gameprofile.models import UserProfile
from xml.etree import ElementTree
import urllib2


class AccountForm(forms.Form):
    steamID = forms.CharField(max_length=100)
    age = forms.IntegerField()
    language = forms.CharField(max_length=100)
    

def display_article(request, book_name, article_title):
    book_name = book_name.replace('-', ' ')
    article_title = article_title.replace('-', ' ')
    art = Article.objects.filter(book__name__iexact=book_name).filter(
                title__iexact=article_title)[0]
    # TODO: art does not exist
    currentNode = Node.objects.filter(article=art)[0]
    nextNode = currentNode.get_next_sibling()
    prevNode = currentNode.get_previous_sibling()
    toc = Node.objects.filter(book__name__iexact=book_name)

    USER = request.user
    username = USER.username
    gameprofile = UserProfile.objects.filter(user=USER)

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

    view_state = 'novice'
    other_state = 'expert'

    # If a steam game, then see if the user has more than 33% of the achievements,
    # if so, then default to the expert view.
    if steamID:
        article_Ach = art.achievements.all()
        total_article_Ach = len(article_Ach)
        total_user_Ach = 0
        for ua in user_ach:
            try:
                if article_Ach.index(ua) >= 0:
                    total_user_Ach = total_user_Ach + 1
            except:
                pass
        percentage_Ach = total_user_Ach / float( total_article_Ach )
        if percentage_Ach >= 0.33:
            view_state = 'expert'
            other_state = 'novice'

    return render_to_response('expertview.html', {'article': art, 'username':username, 'user':USER,
        'next_node': nextNode, 'prev_node': prevNode, 'toc': toc, 'book_name': book_name,
        'view_state': view_state, 'other_state':other_state})


def display_table_of_contents(request, book_name):
    username = request.user.username
    book_name = book_name.replace('-', ' ')
    toc = Node.objects.filter(book__name__iexact=book_name)
  
    book = Book.objects.filter(name__iexact=book_name)[0]

    return render_to_response('book.html', {'toc': toc,
        'book': book, 'username': username, 'user': request.user})


def display_books(request):
    username = request.user.username
    book_list = Book.objects.all()
    ft2_book = book_list.filter(name="Team Fortress 2")[0]
    wow_book = book_list.filter(name="World of Warcraft")[0]
    return render_to_response('library/library.html', {'book_list': book_list, 'user':request.user, 'ft2_book':ft2_book, 'wow_book':wow_book})


def display_tag(request):
    pass


def display_achievements(request):
    pass


def submit_ID(request):
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
            
            print achievements
            return HttpResponseRedirect('/book/display_achievements')  # Redirect after POST
    else:
        form = AccountForm()  # An unbound form

    return render_to_response('test_achievements.html', {
        'form': form,
    }, context_instance=RequestContext(request))
