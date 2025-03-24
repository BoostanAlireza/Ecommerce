from locust import HttpUser, task, between
from random import randint, choice


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    access_token = None
    cart_id = None

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

    # def on_start(self):
    #     login_payload = {
    #         'username': 'admin',
    #         'password': '1'
    #     }
    #     response = self.client.post('/auth/jwt/create/', json=login_payload)
    #     if response.status_code == 200:
    #         self.token = response.json()['token']
    #     else:
    #         print(f'Login failed: {response.status_code}')
    
    # @task()
    # def create_a_cart(self):
    #     if self.token:
    #         headers = {'Authorization': f'Bearer {self.token}'}
    #         response = self.client.post('/store/carts/',
    #                          json={'key': 'value'},
    #                          headers=headers
    #                          )
    #     else:
    #         print("No token available, skipping request")
    #     result = response.json()
    #     self.cart_id = result['id']

def on_start(self):
        """Authenticate and create a cart when the user starts."""
        # Step 1: Get JWT access token
        login_payload = {
            "username": "admin",  # Replace with a valid username
            "password": "1"       # Replace with a valid password
        }
        response = self.client.post(
            "/auth/jwt/create/",
            json=login_payload
        )
        if response.status_code == 200:
            # Extract the access token from the response
            token_data = response.json()
            self.access_token = token_data["access"]
            print(f"Authenticated successfully, access token: {self.access_token[:10]}...")
        else:
            print(f"Authentication failed: {response.status_code} - {response.text}")
            return  # Exit if authentication fails

        # Step 2: Create a cart using the access token
        if self.access_token:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = self.client.post(
                "/store/carts/",
                json={login_payload},  # Adjust payload if your endpoint requires data
                headers=headers
            )
            if response.status_code in (200, 201):
                cart_data = response.json()
                self.cart_id = cart_data.get("id")  # Adjust key if 'id' differs
                print(f"Cart created successfully, ID: {self.cart_id}")
            else:
                print(f"Cart creation failed: {response.status_code} - {response.text}")

@task
def dummy_task(self):
    """Placeholder task to keep Locust running."""
    if self.access_token:
        self.client.get("/store/carts/",  # Adjust endpoint as needed
                        headers={"Authorization": f"Bearer {self.access_token}"},
                        name="/store/carts")
    else:
        print("No access token, skipping task")
