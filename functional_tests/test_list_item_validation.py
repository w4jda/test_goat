from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    # @skip
    def test_cannot_send_empty_items(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector(".has-error").text,
                "You cannot have an empty list item",
            )
        )
        hello = list()
        hello.append("a")
        # she tries again, which now it works

        self.browser.find_element_by_id("id_new_item").send_keys("Buy milk")
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # She tries again to send empty_element
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        # She receives similar warning message

        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector(".has-error").text,
                "You cannot have an empty list item",
            )
        )

        # And she is correcting by putting some text in

        self.browser.find_element_by_id("id_new_item").send_keys("Make tea")
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make tea")
