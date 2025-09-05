window.onload = function() {
    fetch('/getProducts')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector("#productsTable tbody");
        data.forEach(product => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${product.product_id}</td>
                <td>${product.name}</td>
                <td>${product.uom}</td>
                <td>${product.price_per_unit}</td>
                <td><button class="delete-btn" onclick="deleteProduct(${product.product_id})">Delete</button></td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => console.error('Error:', error));
    openForm();


    // ------------------------------------
    fetch('/getOrders')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector("#ordersTable tbody");
        data.forEach(orders => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${orders.order_id}
                <button data-selectedOrderId="${orders.order_id}" class = "openOrderDetailsbtn">Order Details</button>
                </td>
                <td>${orders.customer_name}</td>
                <td>${orders.total}</td>
                <td>${orders.date}</td>
                <td><button class="delete-btn" onclick="deleteOrder(${orders.order_id})">Delete</button>
                
                <button type="button" class="btn btn-primary addOrderDetailBtn" data-toggle="modal" data-target="#exampleModal" data-orderid="${orders.order_id}" >
                    Add an item
                </button>
                
                
                </td>
            `;
            tableBody.appendChild(row);
            

        });

        const addDetailButtons = document.querySelectorAll(".addOrderDetailBtn");
        addDetailButtons.forEach(btn => {
            btn.addEventListener("click", () => {
            const orderId = btn.getAttribute("data-orderid");
            document.getElementById("curOrderIdInput").value = orderId;
            });
        });

        const detailButtons = document.querySelectorAll(".openOrderDetailsbtn");
        detailButtons.forEach(btn => {
            btn.addEventListener("click", () => {
                const orderId = btn.getAttribute("data-selectedOrderId");
                openOrderDetails(orderId);   // poziva tvoju funkciju
                document.getElementById("orderDetailModalID").style.display = "block"; // otvori modal
            });
        });


        // trebam dodat event listener da otvori modal za detalje narudzbe 






    })
    .catch(error => console.error('Error:', error));


    setupTotalPrice() //za modal
};



function deleteProduct(productId) {
    fetch(`/deleteProduct/${productId}`, { method: 'DELETE' })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // document.querySelector(`#row-${productId}`).remove();
            location.reload();
        } else if (data.error) {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}
function deleteOrder(orderId) {
    fetch(`/deleteOrder/${orderId}`, { method: 'DELETE' })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // document.querySelector(`#row-${productId}`).remove();
            location.reload();
        } else if (data.error) {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}

function openOrderDetails(order_id){
    
    fetch(`/openOrderDetails/${order_id}`,{method:'POST'})
    .then(response=>response.json())
    .then(data=>{
        const tableBody = document.querySelector("#orderDetailModalBody");
        tableBody.innerHTML = "";
        const header = document.getElementById("orderDetailHeader")
        header.textContent= data[0][0]
        
        
        data.forEach(detail => {
            const row = document.createElement("tr");
            
            row.innerHTML = `
                <td style="text-align: center;">${detail[1]}</td>
                <td style="text-align: center;">${detail[2]}</td>
                <td style="text-align: center;">${detail[3]}</td>`;
            tableBody.appendChild(row);
        });

        var modal = document.getElementById("orderDetailModalID");


        // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("orderDetailModalClose")[0];

        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
        modal.style.display = "none";
        }

        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
        }
        
    })
}



function openForm(){
    const btnProducts = document.getElementById('submit1');
    const formProducts = document.getElementById('popUpFormProducts');
    const btnOrders = document.getElementById('submit2');
    const formOrders = document.getElementById('popUpFormOrders');

    btnProducts.addEventListener('click', () => {
        if ((formProducts.style.display === 'none' || formProducts.style.display === '') && (formOrders.style.display === 'none' || formOrders.style.display === '')) {
            formProducts.style.display = 'block';
            btnProducts.textContent = "Hide Form";

        } else {
            if((formOrders.style.display != 'none' && formOrders.style.display != '')){
                alert('You have to close orders form first')
                
            }
            else{
                formProducts.style.display = 'none';
                btnProducts.textContent = "Add Product";
            }


        }
    });

    btnOrders.addEventListener('click', () => {
    if ((formOrders.style.display === 'none' || formOrders.style.display === '') && (formProducts.style.display === 'none' || formProducts.style.display === '')) {
        formOrders.style.display = 'block';
        btnOrders.textContent = "Hide Form"; 
  
    
    } else {
        if((formProducts.style.display != 'none' && formProducts.style.display != '')){
            alert('You have to close products form first')
        } 
        else{
            formOrders.style.display = 'none';
            btnOrders.textContent = "Add Order";
        }

 
    }
    });

    
    


}


function setupTotalPrice() {
    const productSelect = document.getElementById("prodID");
    const quantityInput = document.getElementById("quantity");
    const totalPriceInput = document.getElementById("totalPrice");

    function updateTotal() {
        const selectedOption = productSelect.options[productSelect.selectedIndex];
        const pricePerUnit = selectedOption.getAttribute("data-price");
        const quantity = quantityInput.value || 0;
        const total = pricePerUnit * quantity;
        totalPriceInput.value = total;
    }

    
    productSelect.addEventListener("change", updateTotal);
    quantityInput.addEventListener("input", updateTotal);

    
    updateTotal();
}


// function totalOrderPrice(){
//     const btns = document.getElementsByClassName("btn-primary")
    
//     for (let btn of btns) {
//         btn.addEventListener("click", function() {
//             curId = document.getElementById("curOrderIdInput").value;                     
//             fetch(`/changeOrderTotal/${curId}`, { method : 'POST' })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.message) {
                    
//                     location.reload();
//                 } else if (data.error) {
//                     alert('Error: ' + data.error);
//                 }
//             })
//             .catch(error => console.error('Error:', error));
//             });
//         }
// }  







