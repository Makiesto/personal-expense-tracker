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


class ExpenseFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories"
    )
    min_cost = forms.DecimalField(required=False, label="Min Cost")
    max_cost = forms.DecimalField(required=False, label="Max Cost")
