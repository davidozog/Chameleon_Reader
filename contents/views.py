# Create your views here.

from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from models import Article, Node, Book


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
