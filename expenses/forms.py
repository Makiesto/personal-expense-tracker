from django import forms
from .models import Expense, Category


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense_text', 'cost', 'category']
        widgets = {
            'expense_text': forms.TextInput(attrs={'placeholder': 'Expense title'}),
            'cost': forms.NumberInput(attrs={'placeholder': 'Amount'}),
            'category': forms.RadioSelect(),
            'description': forms.CharField(),
        }


