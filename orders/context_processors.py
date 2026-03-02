from orders.session import CartStore


def cart_counter(request):
    """
    Calculate the total quantity of items in the cart
    """
    cart_store = CartStore(request)
    total_quantity = cart_store.count_items()
    return {"cart_total_quantity": total_quantity}
