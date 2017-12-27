from realbrowserlocusts import HeadlessChromeLocust, PhantomJSLocust
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


from locust import TaskSet, task

baseUrl = "http://35.198.133.209/"
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
        self.client.get(baseUrl + "product/beanie/")
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
        self.client.find_element_by_id('billing_first_name').send_keys("Vanessa")
        self.client.find_element_by_id('billing_last_name').send_keys("Beautiful")
        self.client.find_element_by_id('billing_address_1').send_keys("Frankfurter Allee 223")
        self.client.find_element_by_id('billing_postcode').send_keys("10367")
        self.client.find_element_by_id('billing_city').send_keys("Berlin")
        self.client.find_element_by_id('billing_email').send_keys("vanessabelle19@yahoo.com")
        self.client.find_element_by_id('place_order').click()
        self.client.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Order received"]')
            )
        )


    @task(1)
    def homepage_and_docs(self):
        self.client.timed_event_for_locust(
            "Go to", "homepage",
            self.open_locust_homepage
        )
        self.client.timed_event_for_locust(
            "Click to",
            "shop",
            self.click_through_to_shop
        )
        self.client.timed_event_for_locust(
            "Add",
            "product",
            self.make_order_and_checkout
        )




class LocustUser(PhantomJSLocust):

    host = "not really used"
    timeout = 5000  # in seconds in waitUntil thingies
    min_wait = 100
    max_wait = 1000
    screen_width = 1200
    screen_height = 600
    task_set = LocustUserBehavior
