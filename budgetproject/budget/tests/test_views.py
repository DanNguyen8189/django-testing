from django.test import TestCase, Client
#Client import mimics how our client will access our views
from django.urls import reverse
from budget.models import Project, Category, Expense
import json

class TestViews(TestCase):
    def setUp(self):
        #create client instance
        client = Client()
        self.list_url = reverse('list')
        self.detail_url = reverse('detail', args=['project1'])
        self.project1 = Project.objects.create(
            name='project1',
            budget=10000
        )

    def test_project_list_GET(self):
        #send get request to test views! (that's all we need)
        response = self.client.get(self.list_url)
        #make sure that we get status 200
        self.assertEquals(response.status_code, 200)
        #assert that the response contains a certain template
        self.assertTemplateUsed(response, 'budget/project-list.html')

    def test_project_detail_GET(self):
        #send get request to test views! (that's all we need)
        response = self.client.get(self.detail_url)
        #make sure that we get status 200
        self.assertEquals(response.status_code, 200)
        #assert that the response contains a certain template
        self.assertTemplateUsed(response, 'budget/project-detail.html')

    def test_project_detail_POST_adds_new_expense(self):
        Category.objects.create(
            project = self.project1,
            name='development'
        )

        #add a new expense
        response = self.client.post(self.detail_url, {
            'title': 'expense1',
            'amount': 1000,
            'category': 'development'
        })

        #assert that a redirect happened 
        self.assertEquals(response.status_code, 302)
        #assert that expense was added to the project
        self.assertEquals(self.project1.expenses.first().title, 'expense1') #the first() function refers to the first expense added

    def test_project_detail_POST_no_data(self):
        #add a new expense
        response = self.client.post(self.detail_url)

        #assert that a redirect happened 
        self.assertEquals(response.status_code, 302)
        #assert that no expense was added to the project
        self.assertEquals(self.project1.expenses.count(), 0)

    def test_project_detail_DELETE_deletes_expense(self):
        #create expense
        category1 = Category.objects.create(
            project = self.project1,
            name = 'development'
        )
        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 1000,
            category = category1
        )
        #delete expense
        response = self.client.delete(self.detail_url, json.dumps({
            'id' : 1
        }))

        self.assertEquals(response.status_code, 204)
        self.assertEquals(self.project1.expenses.count(), 0)

    def test_project_detail_DELETE_deletes_expense(self):
        #create expense
        category1 = Category.objects.create(
            project = self.project1,
            name = 'development'
        )
        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 1000,
            category = category1
        )
        #delete expense
        response = self.client.delete(self.detail_url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(self.project1.expenses.count(), 1)

    def test_project_create_POST(self):
        url = reverse('add')
        response = self.client.post(url, {
            'name' : 'project2',
            'budget' : 10000,
            'categoriesString' : 'design,development'
        })

        project2 = Project.objects.get(id=2)

        self.assertEquals(project2.name, 'project2')

        #make sure both of the categories we gave the project are there
        first_category = Category.objects.get(id=1)
        self.assertEquals(first_category.project, project2)
        self.assertEquals(first_category.name, 'design')
        second_category = Category.objects.get(id=2)
        self.assertEquals(second_category.project, project2)
        self.assertEquals(second_category.name, 'development')
