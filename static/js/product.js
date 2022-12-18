document.addEventListener("DOMContentLoaded", () => {
    const quantity = document.getElementById("product_qty")
    const decrease = document.getElementById("dec_qty")
    const increase = document.getElementById("inc_qty")
    const addBtn = document.getElementById("add")
    const warning = document.getElementById("qty_warning")
    const stock = document.getElementById("current_stock")

    // Mutation Observer for stock - https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver
    const config = { childList: true }
    const callback = (mutationList, observer) => {
        for (const mutation of mutationList) {
            if (mutation.type === 'childList') {
                updateStock()
                } else {
                console.log(mutation.type)
            }
        }
    }
    const observer = new MutationObserver(callback)
    observer.observe(stock, config)

    decrease.addEventListener("click", decQty)
    increase.addEventListener("click", incQty)

    let qty = Number(quantity.value)
    let currentStock
    warning.style.display = "none"

    // Disable/enable add button, change qty and warning display
    function updateStock() {
        currentStock = stock.textContent
        if (currentStock == "") {
            quantity.value = 0
            addBtn.disabled = true
            warning.style.display = "none"
        } else if (currentStock <= 0) {
            quantity.value = 0
            warning.style.display = "block"
            addBtn.disabled = true
        } else {
            quantity.value = 1
            warning.style.display = "none"
            addBtn.disabled = false
        }        
    }

    // Decrease quantity
    function decQty() {
        if (qty > 1) {
            qty--
            quantity.value = qty
        }
        if (qty < currentStock || qty == 99) {
            warning.style.display = "none"
        }
    }

    // Increase quantity
    function incQty() {
        if (qty < currentStock && qty < 99) {
            qty++
            quantity.value = qty
        }
        if (qty == currentStock || qty == 99) {
            warning.style.display = "block"
        }
    }
})