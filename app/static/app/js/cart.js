var updateBtns = document.getElementsByClassName('update-cart')

for(var i=0;i < updateBtns.length;i++){
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('product',productId,'action',action);
        console.log('productId',productId,'action',action);
        console.log('user:', user)
        if (user==="AnonymousUser"){
            console.log('user not logged in')
        }else {
            
            updateUserOrder(productId,action)

            }
        

    })
}

// Thêm xử lý cho các núttăng/giảm số lượng
document.addEventListener('DOMContentLoaded', function() {
    var quantityBtns = document.querySelectorAll('.btn-quantity');
    
    quantityBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            var action = this.dataset.action;
            var productId = this.closest('.row').dataset.product;
            
            if (user === 'AnonymousUser') {
                console.log('User not logged in');
            } else {
                updateUserOrder(productId, action);
            }
        });
    });
});

function updateUserOrder(productId, action) {
    console.log('Sending data...');
    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // Update cart UI without page reload
        updateCartUI(productId, action);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Có lỗi xảy ra khi cập nhật giỏ hàng');
    });
}

function updateCartUI(productId, action) {
    const row = document.querySelector(`[data-product="${productId}"]`);
    if (!row) return;

    const quantityElement = row.querySelector('.quantity');
    const totalElement = row.querySelector('strong');
    const priceElement = row.querySelector('.text-muted');
    
    let quantity = parseInt(quantityElement.textContent);
    const price = parseFloat(priceElement.textContent.replace(/[^0-9.-]+/g, ''));

    // Update quantity
    if (action === 'add') {
        quantity += 1;
    } else if (action === 'remove') {
        quantity -= 1;
    }

    // Update UI elements
    if (quantity <= 0) {
        row.remove();
    } else {
        quantityElement.textContent = quantity;
        totalElement.textContent = '$' + (price * quantity).toFixed(2);
    }

    // Update cart totals
    updateCartTotals();
}

function updateCartTotals() {
    const quantities = Array.from(document.querySelectorAll('.quantity'))
        .map(el => parseInt(el.textContent));
    const totals = Array.from(document.querySelectorAll('strong'))
        .map(el => parseFloat(el.textContent.replace(/[^0-9.-]+/g, '')));

    const totalItems = quantities.reduce((a, b) => a + b, 0);
    const totalAmount = totals.reduce((a, b) => a + b, 0);

    document.querySelector('.me-4 strong').textContent = totalItems;
    document.querySelector('.me-4:last-of-type strong').textContent = '$' + totalAmount.toFixed(2);
}

    