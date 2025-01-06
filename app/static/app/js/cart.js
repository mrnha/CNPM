var updateBtns = document.getElementsByClassName('update-cart')

for(var i=0;i < updateBtns.length;i++){
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('product',productId,'action',action);
        console.log('user:', user)
        if (user==="AnoymousUser"){
            console.log('user not logged in')
        }else {
            console.log('user logged in, success add')

            }
        

    })
}