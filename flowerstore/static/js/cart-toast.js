(function () {
    const toast = document.getElementById('cart-toast');
    const toastName = document.getElementById('cart-toast-name');
    const toastPrice = document.getElementById('cart-toast-price');
    const toastImage = document.getElementById('cart-toast-image');
    let toastTimer = null;

    function showToast(data) {
        toastName.textContent = data.product_name;
        toastPrice.textContent = data.product_price;
        if (data.product_image) {
            toastImage.src = data.product_image;
            toastImage.alt = data.product_name;
            toastImage.hidden = false;
        } else {
            toastImage.hidden = true;
        }

        // Update cart badge
        const qty = data.cart_total_quantity;
        const cartLinks = document.querySelectorAll('.nav-action-cart');
        cartLinks.forEach(link => {
            let badge = link.querySelector('.nav-action-badge');
            if (qty > 0) {
                if (!badge) {
                    badge = document.createElement('span');
                    badge.className = 'nav-action-badge';
                    link.appendChild(badge);
                }
                badge.textContent = qty;
            }
        });

        toast.hidden = false;
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => { toast.hidden = true; }, 4000);
    }

    document.addEventListener('submit', async function (e) {
        const form = e.target.closest('form[action*="cart/add/"]');
        if (!form) return;
        e.preventDefault();
        try {
            const res = await fetch(form.action, {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                body: new FormData(form),
            });
            const data = await res.json();
            if (data.success) showToast(data);
        } catch {
            form.submit();
        }
    });
})();
