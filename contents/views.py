# Create your views here.

from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from models import Article, Node, Book, Achievement
from django import forms
from xml.etree import ElementTree
import urllib2


class AchievementForm(forms.Form):
    steamID = forms.CharField(max_length=100)


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

    return render_to_response('expertview.html', {'article': art,
        'next_node': nextNode, 'prev_node': prevNode, 'toc': toc, 'book_name': book_name})


def display_table_of_contents(request, book_name):
    username = request.user.username
    book_name = book_name.replace('-', ' ')
    toc = Node.objects.filter(book__name__iexact=book_name)

    return render_to_response('book.html', {'toc': toc,
        'book_name': book_name, 'username': username, 'user': request.user})


def display_books(request):
    username = request.user.username
    book_list = Book.objects.all()
    return render_to_response('library/library.html', {'book_list': book_list})


def display_tag(request):
    pass


def display_achievements(request):
    pass


def submit_ID(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = AchievementForm(request.POST)  # A form bound to the POST data
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
        form = AchievementForm()  # An unbound form

    return render_to_response('test_achievements.html', {
        'form': form,
    }, context_instance=RequestContext(request))
