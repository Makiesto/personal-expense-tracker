from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Expense, UserCategory


class CategoryModelTest(TestCase):
    """Tests for the Category model"""

    def setUp(self):
        self.category = Category.objects.create(name="Food")

    def test_category_creation(self):
        """Test that a category can be created"""
        self.assertEqual(self.category.name, "Food")
        self.assertIsInstance(self.category, Category)

    def test_category_str(self):
        """Test the string representation of category"""
        self.assertEqual(str(self.category), "Food")


class ExpenseModelTest(TestCase):
    """Tests for the Expense model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Transportation")
        self.expense = Expense.objects.create(
            expense_text="Taxi ride",
            cost=Decimal('25.50'),
            category=self.category,
            user=self.user,
            description="Ride to airport"
        )

    def test_expense_creation(self):
        """Test that an expense can be created"""
        self.assertEqual(self.expense.expense_text, "Taxi ride")
        self.assertEqual(self.expense.cost, Decimal('25.50'))
        self.assertEqual(self.expense.category, self.category)
        self.assertEqual(self.expense.user, self.user)

    def test_expense_str(self):
        """Test the string representation of expense"""
        self.assertEqual(str(self.expense), "Taxi ride")


class UserCategoryModelTest(TestCase):
    """Tests for the UserCategory model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Entertainment")
        self.user_category = UserCategory.objects.create(
            user=self.user,
            category=self.category,
            total_expense=Decimal('100.00')
        )

    def test_user_category_creation(self):
        """Test that a user category can be created"""
        self.assertEqual(self.user_category.user, self.user)
        self.assertEqual(self.user_category.category, self.category)
        self.assertEqual(self.user_category.total_expense, Decimal('100.00'))

    def test_user_category_str(self):
        """Test the string representation of user category"""
        expected = f"{self.user.username} - {self.category.name}"
        self.assertEqual(str(self.user_category), expected)


class ViewsTest(TestCase):
    """Tests for views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Utilities")

    def test_home_view_redirect_when_authenticated(self):
        """Test that authenticated users are redirected to dashboard"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('expenses:dashboard'))

    def test_home_view_for_anonymous_user(self):
        """Test that anonymous users see the home page"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/home.html')

    def test_dashboard_requires_login(self):
        """Test that dashboard requires authentication"""
        response = self.client.get(reverse('expenses:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_dashboard_view_for_authenticated_user(self):
        """Test that authenticated users can access dashboard"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('expenses:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/dashboard.html')

    def test_add_expense_requires_login(self):
        """Test that adding expense requires authentication"""
        response = self.client.get(reverse('expenses:add'))
        self.assertEqual(response.status_code, 302)

    def test_add_expense_view(self):
        """Test adding an expense"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('expenses:add'), {
            'expense_text': 'Electric bill',
            'cost': '150.00',
            'category': self.category.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Expense.objects.filter(expense_text='Electric bill').exists())

    def test_category_detail_view(self):
        """Test category detail view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('expenses:detail', kwargs={'category_id': self.category.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/detail.html')


class AuthenticationTest(TestCase):
    """Tests for authentication"""

    def setUp(self):
        self.client = Client()

    def test_signup_view(self):
        """Test signup page loads"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_user_registration(self):
        """Test user can register"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        """Test login page loads"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_user_login(self):
        """Test user can log in"""
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)