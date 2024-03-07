document.addEventListener('DOMContentLoaded', function() {
    var items = document.querySelectorAll('.item');

    items.forEach(function(item) {
        item.addEventListener('click', function() {
            var productName = this.getAttribute('data-name');
            var productDescription = this.getAttribute('data-description');
            var productImage = this.getAttribute('data-image');

            document.querySelector('.section-word').textContent = productName;
            document.querySelector('.section-text2').textContent = productDescription;
            document.getElementById('jam').src = productImage;
            document.getElementById('jam-mobile').src = productImage;
            document.querySelector('.button3').href = '/' + productName;

            items.forEach(function(el) { el.classList.remove('active'); });
            item.classList.add('active');
        });
    });

    if (items.length > 0) {
        items[0].click();
    }
});
