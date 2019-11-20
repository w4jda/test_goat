from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_send_empty_items(self):
        self.fail('write me!')
