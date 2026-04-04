## 🌸 Flower Store — Full-Stack E-commerce Web App

### Project Overview
A team-built online flower shop where customers can browse floral products,
manage a shopping cart, make wish lists, write reviews, and complete secure purchases.
Developed collaboratively using Django's MVT architecture over multiple milestones.

---

### Key Features
- Product browsing with search, sort, and category filtering
- Product reviews with ratings, voting, flagging, and comments
- Shopping cart with real-time item count and quantity management
- Secure checkout via Stripe with billing and shipping address collection
- Webhook-based order fulfillment triggered by payment confirmation
- User authentication with registration, login, account management, and password reset
- Wishlist for saving and transferring products to cart

---

### Tech Stack
| Layer    | Technology                   |
|----------|------------------------------|
| Backend  | Django 6, Python 3.13        |
| Database | SQLite                       |
| Payments | Stripe API + Webhooks        |
| Frontend | HTML, CSS, Django templates  |

---

### Project Structure

```
flowerstore-new/
│
├── flowerstore/               # Project core
│   ├── settings.py            # Database, installed apps, static files
│   ├── urls.py                # Root URLs — routes requests to each app
│   ├── templates/             # Global templates
│   │   ├── base.html          # Parent template for all pages
│   │   └── snippets/
│   │       ├── nav.html
│   │       └── footer.html
│   └── static/css/            # Global CSS
│       ├── base.css
│       ├── nav.css
│       └── ...
│
├── accounts/                  # App 1 — User system: registration, login, logout, profile
│   ├── models.py              # Account (custom user, email login)
│   ├── views.py               # Register, login, logout, profile
│   ├── urls.py
│   ├── forms.py
│   └── templates/accounts/
│
├── products/                  # App 2 — Products: listing, detail, categories, search
│   ├── models.py              # Product, Category
│   ├── views.py               # Index, product detail, category list/detail, search
│   ├── urls.py
│   ├── forms.py
│   └── templates/products/
│
├── orders/                    # App 3 — Cart, Stripe checkout, wishlist
│   ├── models.py              # Order, OrderItem, WishlistItem
│   ├── views.py               # Cart, checkout, wishlist
│   ├── urls.py
│   ├── forms.py
│   ├── session.py             # Cart stored in session (no login required)
│   └── templates/orders/
│
└── reviews/                   # App 4 — Reviews, voting, flagging, comments
    ├── models/                # Split into 4 files
    │   ├── review.py          # Review
    │   ├── vote.py            # Vote
    │   ├── flag.py            # Flag
    │   └── comment.py         # Comment
    ├── views.py
    ├── urls.py
    ├── forms.py
    └── templates/reviews/
```

---

### My Contributions
This is a collaborative team project. https://github.com/582-41B-VA/flowerstore.git

My contributions include:
- **Authentication system** — custom user model (`AbstractBaseUser`), register/login/account page, order history, password reset via email
- **Stripe webhook integration** — order fulfillment, cart clearance, and address handling triggered by payment events
- **Product & browsing foundation** — `Product` and `Category` models, product list/detail/category pages, sort and filter by price/date/name/availability, search results page with combined filters
- **Review voting system** — `Vote` model, upvote/downvote on reviews, live vote count display
- **Shopping cart UX** — cart item count in navigation, cart display and address logic updates
- **Security setup** — moved `SECRET_KEY` and Stripe API keys to `.env`, removed sensitive files from git tracking

---

### Updates I Made
As a solo follow-up, I redesigned and improved the project after the team submission:
- Modernized the UI with a refreshed color palette and typography
- Redesigned layout with clearer visual sections and hierarchy
- Optimized images and media for better performance
- Made the site fully responsive on mobile and smaller screens
- Improved user flow and navigation clarity

---

### Getting Started
To set up the project environment on your local machine, follow these instructions:

```bash
git clone https://github.com/582-41B-VA/flowerstore
cd flowerstore
uv sync
uv run manage.py migrate
uv run manage.py runserver
