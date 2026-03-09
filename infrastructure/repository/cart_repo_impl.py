from domain.repository import CartRepo
from infrastructure import model


class CartRepoImpl(CartRepo):

    def __init__(self, db):
        self.db = db

    def create_cart(self, customer_id):
        cart = model.Cart(customer_id=customer_id)
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart

    def get_cart_by_id(self, customer_id):
        cart = self.db.query(model.Cart).filter(model.Cart.customer_id == customer_id).first()
        return cart

    def add_items_to_cart(self, cart_id, product_id):

        product = self.db.query(model.Product).filter(
            model.Product.product_id == product_id
        ).first()

        item = self.db.query(model.CartItem).filter(
            model.CartItem.cart_id == cart_id,
            model.CartItem.product_id == product_id
        ).first()

        if not item:
            item = model.CartItem(
                cart_id=cart_id,
                product_id=product_id,
                qty=1,
                total_price=product.price
            )

            self.db.add(item)

        else:
            item.qty += 1
            item.total_price = item.qty * product.price

        self.db.commit()
        self.db.refresh(item)

        self.update_cart_amount(cart_id, product.price, True)

        return item

    def view_cart_items(self, cart_id):

        items = self.db \
            .query(model.CartItem, model.Product) \
            .join(model.Product, model.CartItem.product_id == model.Product.product_id) \
            .filter(model.CartItem.cart_id == cart_id) \
            .all()
        result = []

        for cart_item, product in items:
            result.append({
                "item_id": cart_item.item_id,
                "qty": cart_item.qty,
                "total_price": cart_item.total_price,
                "product": {
                    "product_id": product.product_id,
                    "product_name": product.product_name,
                    "price": product.price
                }
            })
        return result

    def delete_cart_items(self, item_id):
        item = self.db.query(model.CartItem).filter(model.CartItem.item_id == item_id).first()
        if not item:
            return
        product_price = item.total_price / item.qty
        cart_id = item.cart_id
        if item.qty > 1:
            item.qty -= 1
            item.total_price = item.qty * product_price
        else:
            self.db.delete(item)
        self.db.commit()
        self.update_cart_amount(cart_id, product_price, False)

    def update_cart_amount(self, cart_id: str, item_price: float, add: bool):
        cart = self.db.query(model.Cart).filter(model.Cart.cart_id == cart_id).first()
        if add:
            cart.amount += item_price
        else:
            cart.amount = max(0, cart.amount - item_price)

        self.db.commit()
