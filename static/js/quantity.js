document.addEventListener("DOMContentLoaded", () => {
    const decrease = document.querySelectorAll(".decrease")
    const increase = document.querySelectorAll(".increase")
    const updateBtn = document.querySelectorAll(".update-btn")

    // Add event listeners to our items in the cart
    decrease.forEach(item => item.addEventListener("click", decQty))
    increase.forEach(item => item.addEventListener("click", incQty))
    updateBtn.forEach(item => item.addEventListener("click", update))

    // Decrease quantity
    function decQty(e) {
        let input = e.target.nextElementSibling
        let qty = Number(input.value)

        if (qty > 1) {
            qty --
            input.value = qty
        }
    }

    // Increase quantity
    function incQty(e) {
        let input = e.target.previousElementSibling
        let qty = Number(input.value)
        let stock = e.target.parentElement.firstElementChild
        let current_stock = Number(stock.value)

        if (qty < current_stock && qty < 99) {
            qty++
            input.value = qty
        }
    }

    // Update item
    function update(e) {
        let form = e.target.previousElementSibling
        form.submit()
    }
})