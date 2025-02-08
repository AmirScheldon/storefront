from locust import HttpUser, task, between
from random import randint


class WebSiteUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(weight=2)
    def view_products_collection(self):
        collection_id = randint(2,5)
        
        self.client.get(f'/store/products/?collection_id={collection_id}',
                        name='/store/products/')
        
    @task(weight=4)
    def view_products(self):
        product_id = randint(1,100)
        
        self.client.get(f'/store/products/{product_id}',
                        name='/store/products/:id')
        
    @task(weight=1)
    def add_to_cart(self):
        # limit numbers to get duplicate products in cart
        product_id = randint(2,10)
        
        self.client.post(f'/store/carts/{self.cart_id}/items/',
                         name='/store/carts/items',
                         json={'product_id':product_id, 'quantity': 1})
        
    @task(weight=3)
    def say_hello(self):
        
        self.client.get('/playground/hello/',
                        name='/playground/hello')
        
    def on_start(self):
        response = self.client.post('/store/carts/')
        result = response.json()
        self.cart_id = result['id'] 