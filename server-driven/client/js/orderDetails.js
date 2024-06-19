document.addEventListener('DOMContentLoaded', function() {
    // Example: Reload the page after 5 seconds
    setTimeout(() => {
        location.reload(); // Reload the current page
    }, 10000);
    
    fetch('http://127.0.0.1:5000/order')
        .then(response => response.json())
        .then(data => {
            displayOrderDetails(data);
        })
        .catch(error => {
            console.error('Error fetching order information:', error);
            displayErrorMessage('Failed to fetch order information. Please try again later.');
        });
});

function displayOrderDetails(orderData) {
    const orderDetailsContainer = document.getElementById('orderDetails');
    orderDetailsContainer.innerHTML = ''; // Clear previous content

    if (orderData && orderData.length > 0) {
        orderData.forEach(order => {
            const orderItem = document.createElement('div');
            orderItem.classList.add('order-item');

            const orderTitle = document.createElement('h2');
            orderTitle.textContent = `Order: ${order.items}`;

            const orderInfo = document.createElement('p');
            orderInfo.textContent = `Customer: ${order.customer}, Total: $${order.total.toFixed(2)}`;

            const removeButton = document.createElement('button');
            removeButton.textContent = 'Remove';
            removeButton.classList.add('remove-button');
            removeButton.addEventListener('click', () => {
                removeOrder(order.id);
            });

            orderItem.appendChild(orderTitle);
            orderItem.appendChild(orderInfo);
            orderItem.appendChild(removeButton);
            orderDetailsContainer.appendChild(orderItem);
        });
    } else {
        displayErrorMessage('No order information available.');
    }
}

function removeOrder(orderId) {
    // Implement logic to remove order from the list or notify server
    console.log(`Removing order with ID ${orderId}`);

    const putData = {
        remove_order: orderId
    };
    
    fetch('http://127.0.0.1:5000/order', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(putData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse JSON data from the response
    })
    .then(data => {
        console.log('PUT request successful. Response:', data);
        // Process the response data
    })
    .catch(error => {
        console.error('PUT request failed:', error);
        // Handle errors
    });
    refresh()
    
}

function displayErrorMessage(message) {
    const orderDetailsContainer = document.getElementById('orderDetails');
    orderDetailsContainer.innerHTML = `<p class="error">${message}</p>`;
}

function refresh() {    
    setTimeout(function () {
        location.reload()
    }, 100);
}