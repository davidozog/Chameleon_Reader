from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Book(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)
    book = models.ForeignKey(Book)

    def __unicode__(self):
        return self.name


class Achievement(models.Model):
    name = models.CharField(max_length=50)
    book = models.ForeignKey(Book)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    content = models.TextField()
    title = models.CharField(max_length=200)
    restriction = models.IntegerField(blank=True, null=True)
    references = models.TextField(blank=True, null=True)
    achievements = models.ManyToManyField(Achievement, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    book = models.ForeignKey(Book)

    def __unicode__(self):
        return self.title

# class Concept(models.Model):
#     '''
#     Used to provide tooltips and reference links.
#     '''
#     term = models.CharField(max_length=50)
#     definition = models.TextField()


# class User(models.Model):
#     age = models.IntegerField()
#     achievements = models.ManyToManyField(Achievement)
#     language = models.charField(max_length=20)
#     # highlightings = how to write one to many?
#     # comments = agian, one to many


# class Sequence(models.Model):
#     '''
#     Use <sequence> sequence name </sequence> to refer to a sequence in an Article
#     '''
#     name = models.CharField(max_length=200)
#     article_list = models.ForeignKey(Article)

class Node(MPTTModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    book = models.ForeignKey(Book)
    article = models.ForeignKey(Article, null=True, blank=True)
    order = models.IntegerField(default=1)

    # recursive data type. one of the following has to be null.
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        if self.article:
            return self.article.__unicode__()
        else:
            return self.name
