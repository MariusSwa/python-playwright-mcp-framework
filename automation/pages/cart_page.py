from playwright.sync_api import Page

from core.base_page import BasePage


class CartPage(BasePage):
    PAGE_HEADER = "Cart"
    PRODUCT_IDS = {
        "Wireless Mouse": "wireless-mouse",
        "Mechanical Keyboard": "mechanical-keyboard",
        "USB-C Hub": "usb-c-hub",
        "Laptop Stand": "laptop-stand",
    }

    EMPTY_CART_MESSAGE = {
        "type": "text",
        "value": "Your cart is empty.",
    }

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self, base_url: str) -> None:
        self.goto(f"{base_url.rstrip('/')}/cart.html")

    def cart_item(self, product_name: str) -> dict:
        product_id = self._get_product_id(product_name)
        return {
            "type": "test_id",
            "value": f"cart-item-{product_id}",
        }

    def cart_item_heading(self, product_name: str) -> dict:
        return {
            "type": "role",
            "role": "heading",
            "name": product_name,
            "exact": True,
            "parent": self.cart_item(product_name),
        }

    def remove_button(self, product_name: str) -> dict:
        return {
            "type": "role",
            "role": "button",
            "name": "Remove",
            "exact": True,
            "parent": self.cart_item(product_name),
        }

    def remove_product(self, product_name: str) -> None:
        self.click(self.remove_button(product_name))

    def assert_page_loaded(self) -> None:
        self.assert_heading(self.PAGE_HEADER)

    def assert_cart_is_empty(self) -> None:
        self.expect_visible(self.EMPTY_CART_MESSAGE)

    def assert_product_is_displayed(self, product_name: str) -> None:
        self.expect_visible(self.cart_item_heading(product_name))

    def _get_product_id(self, product_name: str) -> str:
        try:
            return self.PRODUCT_IDS[product_name]
        except KeyError as error:
            raise ValueError(f"Unknown product: {product_name}") from error
