## 🌸 Flower Store — Full-Stack E-commerce Web App

### Project Overview
A team-built online flower shop where customers can browse floral products,
manage a shopping cart, make wish lists, write reviews, and complete secure purchases.
Developed collaboratively using Django's MVT architecture over multiple milestones.

---

### Key Features
- Product browsing with search, sort, and category filtering
- User authentication with registration, login, and account management
- Persistent shopping cart and wishlist
- Stripe payment integration with webhook-based order fulfillment
- Product review and voting system
- Password reset via email

---

### Tech Stack
| Layer    | Technology                   |
|----------|------------------------------|
| Backend  | Django 6, Python 3.13        |
| Database | SQLite (dev)                 |
| Payments | Stripe API + Webhooks        |
| Frontend | HTML, CSS (Django templates) |
| Tools    | uv, Ruff, python-dotenv      |

---

### My Contributions
This is a collaborative team project. My contributions include:
- **Authentication system** — custom user model (`AbstractBaseUser`), login/register/account page, password reset via email
- **Stripe webhook integration** — order fulfillment, cart clearance, and address handling triggered by payment events
- **Review voting system** — `Vote` model, upvote/downvote on reviews, live vote count display
- **Shopping cart UX** — persistent cart item count in navigation, cart display updates
- **Security setup** — moved `SECRET_KEY` and API keys to `.env`, removed sensitive files from git tracking

---

### My Future Updates
Planning to improve the project with the following enhancements:
- Modernize the UI with a refreshed color palette and typography
- Redesign layout with clearer visual sections and hierarchy
- Optimize images and media for better performance
- Make the site fully responsive on mobile and smaller screens
- Improve user flow and navigation clarity

---

### Getting Started
To set up the project environment on your local machine, follow these instructions:

```bash
git clone https://github.com/582-41B-VA/flowerstore
cd flowerstore
uv sync
uv run manage.py migrate
uv run manage.py runserver
