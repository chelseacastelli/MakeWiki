from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.text import slugify

from wiki.forms import PageForm
from wiki.models import Page


class PageCreateView(CreateView):
    '''Create a new wiki page'''
    model = Page
    fields = ['title', 'content', 'author']
    template_name = 'create_page.html'


class PageListView(ListView):
    """ Renders a list of all Pages. """
    model = Page

    def get(self, request):
        """ GET a list of Pages. """
        pages = self.get_queryset().all()
        return render(request, 'list.html', {
          'pages': pages
        })


class PageDetailView(DetailView):
    """ Renders a specific page based on it's slug."""
    model = Page

    def get(self, request, slug):
        """ Returns a specific wiki page by slug. """
        page = self.get_queryset().get(slug__iexact=slug)
        return render(request, 'page.html', {
          'page': page
        })

    def post(self, req, slug):
        '''Edit the page's information'''
        form = PageForm(req.POST)  # create a form

        page = self.get_queryset().get(slug__iexact=slug)
        page.title = req.POST['title']  # retrieve the page's title
        page.content = req.POST['content']  # retrieve the page's content
        page.author = req.user  # get the author of the user
        page.slug = slugify(page.title)  # create a new slug to match title
        page.save()  # saves our new post

        # We load the wiki details page and the url will be the title's slug
        return HttpResponseRedirect(reverse('wiki-details-page', args=[page.slug]))


