
from django.test import SimpleTestCase
from budget.forms import ExpenseForm

class TestForms(SimpleTestCase):
    def test_expense_form_valid_data(self):
        #make a form
        form = ExpenseForm(data = {
            'title': 'expense1',
            'amount': 1000,
            'category' : 'development'
        })

        self.assertTrue(form.is_valid())

    def test_expense_form_invalid_data(self):
        #make a form
        form = ExpenseForm(data={})
        self.assertFalse(form.is_valid())
        #make sure there are 3 errors; one for every field missing
        self.assertEquals(len(form.errors), 3)