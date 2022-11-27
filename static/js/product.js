document.addEventListener("DOMContentLoaded", () => {
    console.log("updated")
    const quantity = document.getElementById("product_qty")
    const decrease = document.getElementById("dec_qty")
    const increase = document.getElementById("inc_qty")
    const prices = document.getElementById("prices")
    const addBtn = document.getElementById("add")
    const warning = document.getElementById("qty_warning")
    const stock = document.getElementById("current_stock")

    // Mutation Observer for stock - https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver
    // FIVE HOURS TO FIND A SOLUTION NOT INVOLVING jQuery
    const config = { childList: true }
    const callback = (mutationList, observer) => {
        for (const mutation of mutationList) {
            if (mutation.type === 'childList') {
                console.log("childList")
                updateStock()
                } else {
                console.log(mutation.type)
            }
        }
    }
    const observer = new MutationObserver(callback)
    observer.observe(stock, config)

    prices.addEventListener("change", changeAddBtn)

    function changeAddBtn() {
        if (prices.value == "default") {
            addBtn.disabled = true
        } else {
            addBtn.disabled = false
        }
    }

    decrease.addEventListener("click", decQty)
    increase.addEventListener("click", incQty)

    let qty = Number(quantity.value)
    let currentStock

    function updateStock() {
        currentStock = stock.textContent
    }

    if (currentStock == 0) {
        quantity.value = 0
        warning.style.display = "block"
    } else {
        warning.style.display = "none"
    }

    function decQty() {
        if (qty > 1) {
            qty--
            quantity.value = qty
        }
        if (qty < currentStock || qty == 99) {
            warning.style.display = "none"
        }
    }

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