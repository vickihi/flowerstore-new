def cart_counter(request):
    """
    Calculate the total quantity of items in the cart
    """
    cart = request.session.get('cart', {})
    total_quantity = sum(cart.values()) if cart else 0
    return {
        'cart_total_quantity': total_quantity
    }