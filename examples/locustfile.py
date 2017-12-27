from realbrowserlocusts import HeadlessChromeLocust, PhantomJSLocust
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import random


from locust import TaskSet, task

baseUrl = "http://35.198.145.216/"
products = ['beanie', 'belt', 'cap', 'sunglasses', 'hoodie-with-logo', 'hoodie-with-pocket', 'hoodie-with-zipper', 'hoodie', 'long-sleeve-tee', 'polo', 'tshirt', 'vneck-tshirt', 'woo-logo', 'woo-album-1', 'woo-album-2', 'woo-album-3', 'woo-single-1', 'woo-album-4', 'woo-single-2', 'woo-logo', 'premium-quality', 'ship-your-idea', 'ninja-silhouette', 'woo-ninja', 'happy-ninja', 'ship-your-idea', 'woo-ninja', 'patient-ninja', 'happy-ninja', 'ninja-silhouette', 'woo-logo', 'flying-ninja', 'premium-quality', 'woo-ninja']
firstNames = ['Sara', 'Maria', 'Juicy', 'Meron','Christmas','Vanessa']
lastNames = ['Michaels', 'Jordan', 'Clinton', 'Blunt', 'Harvey', 'Muller', 'Redfern']

class LocustUserBehavior(TaskSet):

    def open_locust_homepage(self):
        self.client.get(baseUrl)
        self.client.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//a[text()="Shop"]')
            )
        )

    def click_through_to_shop(self):
        self.client\
            .find_element_by_xpath('//a[text()="Shop"]').click()
        self.client.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Shop"]')
            )
        )

    def make_order_and_checkout(self):
        self.client.get(baseUrl + "product/beanie")
        self.client.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Beanie"]')
            )
        )
        self.client.find_element_by_name('add-to-cart').click()
        self.client.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//a[text()="View cart"]')
            )
        )
        self.client.get(baseUrl + "checkout")
        self.client.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Checkout"]')
            )
        )
        self.client.find_element_by_id('billing_first_name').send_keys(random.choice(firstNames))
        self.client.find_element_by_id('billing_last_name').send_keys(random.choice(lastNames))
        self.client.find_element_by_id('billing_address_1').send_keys("Frankfurter Allee 223")
        self.client.find_element_by_id('billing_postcode').send_keys("10367")
        self.client.find_element_by_id('billing_city').send_keys("Berlin")
        self.client.find_element_by_id('billing_email').send_keys("testing@yahoo.com")
        self.client.find_element_by_id('place_order').click()
        self.client.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Order received"]')
            )
        )


    @task(1)
    def homepage(self):
        self.client.timed_event_for_locust(
            "Go to", "homepage",
            self.open_locust_homepage
        )

    @task(2)
    def browse_products(self):
        self.client.timed_event_for_locust(
            "Click to",
            "shop",
            self.click_through_to_shop
        )

    @task(3)
    def add_to_cart_and_checkout(self):
        self.client.timed_event_for_locust(
            "Add",
            "product and checkout",
            self.make_order_and_checkout
        )

class LocustUser(PhantomJSLocust):

    host = "not really used"
    timeout = 180  # in seconds in waitUntil thingies
    stop_timeout = 300
    min_wait = 0
    max_wait = 0
    screen_width = 1200
    screen_height = 1200
    task_set = LocustUserBehavior
