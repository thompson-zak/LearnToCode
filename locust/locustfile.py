import time
from locust import HttpUser, task, between
import json

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def execute_code(self):
        self.client.post("/execute/code", json={"code": "units_sold = 100\nprice_per_unit = 10\n\ntotal_revenue = units_sold * price_per_unit\n\nprint(\"Total sales revenue: $\", total_revenue)"})

    def on_start(self):
        response = self.client.get("/login", headers={"Auth-Header":"CODEAI2024"})
        auth_token = json.loads(response._content)['token']
        self.client.headers = {'Auth-Header': auth_token}
        self.client.get("?section=Variables&id=-1&track=Business")