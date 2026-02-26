// Live Search
const searchInput = document.querySelector("input[name='search']");
const cards = document.querySelectorAll(".card");

if (searchInput) {
    searchInput.addEventListener("keyup", function () {
        let value = this.value.toLowerCase();

        cards.forEach(card => {
            let text = card.innerText.toLowerCase();
            card.style.display = text.includes(value) ? "block" : "none";
        });
    });
}

// Bookmark UI effect
const saveButtons = document.querySelectorAll(".save");

saveButtons.forEach(btn => {
    btn.addEventListener("click", function () {
        this.innerHTML = "✅ Saved";
        this.style.background = "green";
    });
});