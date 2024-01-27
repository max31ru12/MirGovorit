from django.test import TestCase


# Create your tests here.
class TestAddProductToRecipe(TestCase):

    def test_get(self):
        response = self.client.get('/add_product_to_recipe/1/1/120/')
        self.assertEqual(response.status_code, "200")
