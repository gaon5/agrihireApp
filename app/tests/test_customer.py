



    

    # ... rest of your test methods ...


import pytest
from flask_testing import TestCase
from app import app, sql_function
from unittest.mock import patch
from unittest import TestCase

class TestCustomer(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app
    
    
    def setUp(self):
        self.connection = sql_function.get_cursor()
        self.connection.start_transaction()

    def tearDown(self):
        self.connection.rollback()
        self.connection.close()

    
    def test_equipments(self):
        # Mocking the sql_function calls if necessary
        # ...

        # Sending a test request to the equipments route
        response = self.client.get('/equipments')
        self.assertEqual(response.status_code, 200)
        # Further assertions can be made based on the expected behavior of the function
        # ...

    def test_faq(self):
        response = self.client.get('/faq')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('customer/faq.html')
    
    def test_contact_get(self):
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('customer/contact.html')


    def test_contact_post_success(self):
        with patch('app.sql_function.insert_enquiry') as mock_insert:
            mock_insert.return_value = True  # Simulate successful database insert
            form_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'phone': '1234567890',
                'location': 'New York',
                'enquiry_type': 'General',
                'enquiry_details': 'I need help.'
            }
            response = self.client.post('/contact', data=form_data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Your enquiry has been submitted successfully!", response.data)

    def test_contact_post_failure(self):
        with patch('app.sql_function.insert_enquiry') as mock_insert:
            mock_insert.return_value = False  # Simulate failed database insert
            form_data = {
                'first_name': 'Jane',
                'last_name': 'Doe',
                'email': 'jane.doe@example.com',
                'phone': '0987654321',
                'location': 'Los Angeles',
                'enquiry_type': 'Technical',
                'enquiry_details': 'The website is down.'
            }
            response = self.client.post('/contact', data=form_data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"There was an error submitting your enquiry. Please try again.", response.data)




if __name__ == '__main__':
    pytest.main()
