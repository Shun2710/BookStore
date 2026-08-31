class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")

        if not cart:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, book, quantity=1):
        book_id = str(book.id)

        if book_id not in self.cart:
            self.cart[book_id] = {
                "quantity": 0,
                "price": str(book.price),
            }

        self.cart[book_id]["quantity"] += quantity
        self.session.modified = True

    def remove(self, book):
        book_id = str(book.id)

        if book_id in self.cart:
            del self.cart[book_id]
            self.session.modified = True

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True