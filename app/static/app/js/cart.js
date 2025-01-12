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
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        location.reload(); // Reload để cập nhật UI
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

    