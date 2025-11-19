from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from .forms import ExpenseForm, ExpenseFilterForm
from .models import Category, Expense, UserCategory

from . filters import ProductFilter

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('expenses:dashboard')
    else:
        return render(request, "expenses/home.html")


@login_required
def dashboard(request):
    categories = Category.objects.annotate(
        total=Sum('expense__cost', filter=Q(expense__user=request.user))
    )

    expenses_list = Expense.objects.filter(user=request.user)

    expense_filter = ProductFilter(request.GET, queryset=expenses_list)

    context = {
        "categories": categories,
        "expenses_list": expenses_list,
        "filter": expense_filter,
    }

    return render(request, "expenses/dashboard.html", context)


@login_required
def detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, "expenses/detail.html", {"category": category})


@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            user_cat, created = UserCategory.objects.get_or_create(
                user=request.user,
                category=expense.category
            )

            user_cat.total_expense += expense.cost
            user_cat.save()

            return redirect('expenses:dashboard')
    else:
        form = ExpenseForm()

    return render(request, "expenses/add.html", {"form": form})


@login_required
def remove_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == "POST":
        user_cat = UserCategory.objects.get(
            user=request.user,
            category=expense.category
        )

        user_cat.total_expense -= expense.cost
        user_cat.save()

        expense.delete()

        return redirect('expenses:dashboard')

    return render(request, "expenses/confirm_delete.html", {"expense": expense})


@login_required
def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("expenses:detail", category_id=expense.category.id)

    else:
        form = ExpenseForm(instance=expense)

    return render(request, "expenses/update.html", {"form": form})


def root_redirect(request):
    return redirect('login')


# second way to create index view (learning purposes)

# class IndexView(generic.ListView):
#     template_name = "expenses/dashboard.html"
#     context_object_name = "latest_category_list"
#
#     def get_queryset(self):
#         return Category.objects.order_by("-category_text")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         expenses_list = Expense.objects.filter(user=self.request.user)
#
#         category_totals = {}
#         for category in context["latest_category_list"]:
#             total = expenses_list.filter(category=category).aggregate(Sum("cost"))["cost__sum"] or 0
#             category_totals[category.id] = total
#
#         context["expenses_list"] = expenses_list
#         context["category_totals"] = category_totals
#         return context


class DetailView(generic.DetailView):
    model = Category
    template_name = "expenses/detail.html"
