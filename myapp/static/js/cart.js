
var updateBtns = document.getElementsByClassName('update-cart')

for(i=0 ; i < updateBtns.length ; i++){
    updateBtns[i].addEventListener('click', function(){

        var productId = this.dataset.id
        var action = this.dataset.action
        var quantity = $('#numCart').val()
        console.log('productId', productId, 'action', action, 'quantity', quantity)
        if (!quantity){
            quantity=1
        }
        if(user === 'AnonymousUser' ){
            addCookieItem(productId, action, quantity)
        }else{
            console.log('User is login, send data')
            updateUserOrder(productId, action, quantity)
        }
    })
}
function addCookieItem(productId, action, quantity){
    console.log('User is not login')
    if (action=='add'){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity':quantity}
        }else{
            cart[productId]['quantity'] += quantity
        }
    }

    if (action == 'remove'){
        cart[productId]['quantity'] -=1
        if (cart[productId]['quantity'] <= 0){
            console.log(('Item should be deleted'))
            delete cart[productId]
        }
    }
    console.log('Cart', cart)
    document.cookie = 'Cart=' + JSON.stringify(cart) + ";domain=; path=/"

}
function updateUserOrder(productId, action, quantity){
    console.log('User is logged in, sending data...')

    var url= base_url+'update_item'

    fetch(url, {
        method:'POST',
        headers:{
        'Content-Type': 'application/json',
        'X-CSRFToken':csrftoken,

        },
        body:JSON.stringify({'productId':productId, 'action':action, 'quantity':quantity})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        location.reload()
    })
}

$('.chg-quantity').click(function (){
    setTimeout(function(){ window.location.reload();}, 100);
})

