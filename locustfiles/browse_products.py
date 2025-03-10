from locust import HttpUser, task, between
from random import randint, choice


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(2)
    def view_products(self):
        category_id = randint(1, 10)
        self.client.get(
            f'/store/products/?category_id={category_id}',
            name='/store/products'
        )

    @task(4)
    def view_product_details(self):
        product_id = randint(1, 1000)
        self.client.get(
            f'/store/products/{product_id}',
            name='/store/products/:id'
        )

    @task(1)
    def add_to_cart(self):
        product_id = randint(1, 10)
        response = self.client.post(
            f'/store/carts/{self.cart_id}/items/',
            name='/store/carts/items',
            json={'product': product_id, 'quantity': 1}
        )
        print('Response:', response.status_code, response.text)

    def on_start(self):
        response = self.client.post('/store/carts/')
        result = response.json()
        self.cart_id = result['id']
