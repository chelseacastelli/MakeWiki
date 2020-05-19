from django.test import TestCase
from django.contrib.auth.models import User
from wiki.models import Page
from django.utils.text import slugify


class WikiTests(TestCase):
    def test_edit_page(self):
        # Create a new user
        user = User.objects.create_user(
            username='chelly', password='meatloaf9')

        self.client.login(username='chelly', password='meatloaf9')

        # Create our page
        page = Page.objects.create(
            title='Mexican food FTW', content='Cuz it\'s true', author=user)
        page.save()

        # Update data
        post_data = {
            'title': 'At home workouts to do during quarantine',
            'content': 'Grab your dumbbells',
            'author': user.id
        }

        # Create a post request with our new data
        res = self.client.post(f'/{slugify(page.title)}/', post_data)

        # Check that the response code was sent properly
        self.assertEqual(res.status_code, 302)

        updated_data = Page.objects.get(title=post_data['title'])
        # Check that our post data went through and updated the page
        self.assertEqual(updated_data.title, 'At home workouts to do during quarantine')

    def test_detail_page(self):
        # Instance of user to test the pages
        user = User.objects.create()

        # Create a test detail page
        page = Page.objects.create(title="Puppies",
                                   content="Cute & cuddly", author=user)
        page.save()

        # Making a GET request to get our test detail page
        res = self.client.get(f'/{slugify(page.title)}/')

        # Very a 200 response
        self.assertEqual(res.status_code, 200)
        # Check if the page contains our title
        self.assertContains(res, 'Puppies')

    def test_create_page(self):
        # Instance of user to test the pages
        user = User.objects.create()

        # Post data to be sent via the form
        post_data = {
            'title': 'Chocolate pudding pie',
            'content': 'The best...',
            'author': user.id
        }

        # Request to create a post
        res = self.client.post('/create/', data=post_data)

        # Verify our response
        self.assertEqual(res.status_code, 302)

        # Get object to test
        page_object = Page.objects.get(title='Chocolate pudding pie')

        # Check that the page object was created
        self.assertEqual(page_object.title, 'Chocolate pudding pie')