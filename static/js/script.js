
;(function () {
    const chilliModal = new bootstrap.Modal(document.getElementById("chilli-modal"))
  
    htmx.on("htmx:afterSwap", (e) => {
      // Response targeting #dialog => show the modal
      if (e.detail.target.id == "dialog") {
        chilliModal.show()
      }
    })
  
    htmx.on("htmx:beforeSwap", (e) => {
      // Empty response targeting #dialog => hide the modal
      if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
        chilliModal.hide()
        location.reload()
        e.detail.shouldSwap = false
      }
    })
  
    // Remove dialog content after hiding
    htmx.on("hidden.bs.modal", () => {
      document.getElementById("dialog").innerHTML = ""
    })
  })()