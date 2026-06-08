from playwright.sync_api import Page

from core.base_page import BasePage


class ProductsPage(BasePage):
    PAGE_HEADER = "Products"
    PRODUCT_IDS = {
        "Wireless Mouse": "wireless-mouse",
        "Mechanical Keyboard": "mechanical-keyboard",
        "USB-C Hub": "usb-c-hub",
        "Laptop Stand": "laptop-stand",
    }

    PRODUCT_MESSAGE = {
        "type": "test_id",
        "value": "product-message",
    }

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self, base_url: str) -> None:
        self.goto(f"{base_url.rstrip('/')}/products.html")

    def product_card(self, product_name: str) -> dict:
        product_id = self._get_product_id(product_name)
        return {
            "type": "test_id",
            "value": f"product-{product_id}",
        }

    def product_heading(self, product_name: str) -> dict:
        return {
            "type": "role",
            "role": "heading",
            "name": product_name,
            "exact": True,
            "parent": self.product_card(product_name),
        }

    def add_to_cart_button(self, product_name: str) -> dict:
        return {
            "type": "role",
            "role": "button",
            "name": "Add to Cart",
            "exact": True,
            "parent": self.product_card(product_name),
        }

    def add_product_to_cart(self, product_name: str) -> None:
        self.click(self.add_to_cart_button(product_name))

    def assert_page_loaded(self) -> None:
        self.assert_heading(self.PAGE_HEADER)
        self.expect_visible(self.product_heading("Wireless Mouse"))

    def assert_product_is_displayed(self, product_name: str) -> None:
        self.expect_visible(self.product_heading(product_name))

    def assert_product_added(self, product_name: str) -> None:
        self.expect_text(self.PRODUCT_MESSAGE, f"{product_name} added to cart.")

    def _get_product_id(self, product_name: str) -> str:
        try:
            return self.PRODUCT_IDS[product_name]
        except KeyError as error:
            raise ValueError(f"Unknown product: {product_name}") from error
