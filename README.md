# Personal Expense Tracker

A Django-based web application for tracking personal expenses across multiple categories with user authentication and filtering capabilities.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.2.7-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

-  **User Authentication**: Secure signup, login, and logout functionality
-  **Expense Management**: Create, read, update, and delete expenses
-  **Category Organization**: Organize expenses into customizable categories
-  **Advanced Filtering**: Filter expenses by category and cost range
-  **Category Totals**: Automatic calculation of total spending per category
-  **User Isolation**: Each user's data is private and secure
-  **Password Management**: Change password and reset password functionality

## Tech Stack

- **Backend**: Django 5.2.7
- **Database**: SQLite (development)
- **Filtering**: django-filter 25.2
- **CI/CD**: GitHub Actions
- **Frontend**: Django Templates, HTML, CSS

## Project Structure

```
personal_expense_tracker/
├── accounts/                 # User authentication app
│   ├── views.py             # Signup view
│   └── urls.py              # Auth URLs
├── expenses/                 # Main expense tracking app
│   ├── models.py            # Category, Expense, UserCategory models
│   ├── views.py             # CRUD operations and filtering
│   ├── forms.py             # Django forms
│   ├── filters.py           # django-filter configurations
│   └── templates/           # HTML templates
├── templates/registration/   # Authentication templates
├── personal_expense_tracker/ # Project settings
│   ├── settings.py          # Django configuration
│   └── urls.py              # URL routing
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```

## Installation

### Prerequisites

- Python 3.11 or higher
- pip
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Makiesto/personal_expense_tracker.git
   cd personal_expense_tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (IMPORTANT for production)
   
   Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Create categories** (via Django admin)
   ```bash
   python manage.py runserver
   ```
   - Navigate to `http://127.0.0.1:8000/admin`
   - Login with your superuser credentials
   - Add categories (e.g., Food, Transportation, Entertainment, Utilities)

8. **Start the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`

## Usage

### Creating an Account
1. Navigate to the home page
2. Click "Sign up"
3. Fill in your username and password
4. Click "Sign Up"

### Adding Expenses
1. Log in to your account
2. Click "Add expenses" on the dashboard
3. Fill in the expense details:
   - Expense title
   - Amount
   - Category (select from radio buttons)
4. Click "Add Expense"

### Viewing Expenses
- **Dashboard**: View all your expenses and category totals
- **Category Detail**: Click on a category name to see all expenses in that category

### Filtering Expenses
1. On the dashboard, use the filter form
2. Filter by:
   - Category
   - Minimum cost
   - Maximum cost
3. Click "Filter" to apply

### Updating/Deleting Expenses
- Navigate to a category detail page
- Click "Update" to modify an expense
- Click "Remove" to delete an expense (confirmation required)

## Database Models

### Category
- `name`: Category name (e.g., Food, Transportation)

### Expense
- `expense_text`: Title of the expense
- `cost`: Amount spent (decimal)
- `category`: Foreign key to Category
- `user`: Foreign key to User
- `description`: Optional description
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### UserCategory
- `user`: Foreign key to User
- `category`: Foreign key to Category
- `total_expense`: Aggregated total for user-category combination

## Testing

Run the test suite:
```bash
python manage.py test
```

## CI/CD

The project includes a GitHub Actions workflow that:
- Runs on push and pull requests to the main branch
- Sets up Python 3.11
- Installs dependencies
- Runs migrations
- Executes tests

## Known Issues & Future Improvements

### Known Issues
1. ⚠️ **Update expense bug**: When updating an expense's cost or category, the `UserCategory.total_expense` doesn't recalculate
2. Empty password change templates
3. Missing description field in expense form

### Planned Improvements
- [ ] Add data visualization (charts and graphs)
- [ ] Export expenses to CSV/PDF
- [ ] Budget setting and alerts
- [ ] Recurring expenses
- [ ] Mobile-responsive design
- [ ] Dark mode
- [ ] Multi-currency support
- [ ] Receipt image upload

## Security Notes

⚠️ **IMPORTANT**: Before deploying to production:

1. **Change SECRET_KEY**: Never use the default secret key in production
2. **Set DEBUG = False** in settings.py
3. **Configure ALLOWED_HOSTS** with your domain
4. **Use environment variables** for sensitive data
5. **Use PostgreSQL** instead of SQLite for production
6. **Set up HTTPS** with SSL certificates
7. **Configure email backend** for password reset functionality

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Mateusz - [GitHub Profile](https://github.com/makiesto)

## Acknowledgments

- Django Documentation
- django-filter library

## Screenshots

*Add screenshots of your application here*

Example structure:
```
### Dashboard
![Dashboard](screenshots/dashboard.png)

### Add Expense
![Add Expense](screenshots/add-expense.png)

### Category Detail
![Category Detail](screenshots/category-detail.png)
```

## Contact

For questions or feedback, please reach out:
- Email: mateusz.stojek@proton.me
- [LinkedIn](https://www.linkedin.com/in/mateusz-stojek-733957288/)

---

**Note**: This is a learning project demonstrating Django fundamentals, user authentication, and database relationships. It is suitable for portfolio purposes and further development.
