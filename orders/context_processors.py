from orders.session import CartStore
from orders.models import WishlistItem


def cart_counter(request):
    """
    Calculate the total quantity of items in the cart and wishlist.
    """
    cart_store = CartStore(request)
    total_quantity = cart_store.count_items()

    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = WishlistItem.objects.filter(user=request.user).count()

    return {
        "cart_total_quantity": total_quantity,
        "wishlist_count": wishlist_count,
    }
