// need to update once customize-item on the server side is written
async function customizeItem(var1, var2) {
    const res = await fetch("/customize-item", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            var1: input_var1,
            var2: input_var2,
        }),
    });
    const { var3: output_var1, var4: output_var2 } = await res.json();
    const cartItems = document.getElementById('cart-items');
    const li = document.createElement('li');
    li.textContent = var3;
    cartItems.appendChild(li);
    return { var3, var4 };
}

function addToCart(item, price) {
    const cartItems = document.getElementById('cart-items');
    const li = document.createElement('li');
    li.innerHTML = `
        <button class="cart button1" onclick="removeItem(this)">X</button>
        <span>${item}</span>
        <span>$${price}</span>    
    `;
    cartItems.appendChild(li);
}

function submitOrder() {
    const cartItems = document.getElementById('cart-items');
    const items = cartItems.querySelectorAll('li');
    const order = Array.from(items).map(li => li.textContent).join(', ');
    sessionStorage.setItem('order', order); // Store order in session storage
    window.location.href = 'confirmation.html'; // Redirect to confirmation page
}

function clearOrder() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = ''; // Clear cart items
}

function removeItem(item) {
    listItem = item.parentNode;
    list = listItem.parentNode;         
    list.removeChild(listItem);
}