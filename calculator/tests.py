import json

from django.test import TestCase
from django.urls import reverse

from .models import Calculation


class CalculatorTests(TestCase):
    def test_calculator_page_renders(self):
        response = self.client.get(reverse('calculator:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Simple Calculator')

    def test_supported_operations_are_calculated_and_saved(self):
        cases = [
            ('+', '2', '3', '5'),
            ('-', '9', '4', '5'),
            ('*', '1.5', '4', '6'),
            ('/', '7', '2', '3.5'),
        ]

        for operator, left, right, expected in cases:
            with self.subTest(operator=operator):
                response = self.client.post(
                    reverse('calculator:calculate'),
                    data=json.dumps(
                        {'left': left, 'operator': operator, 'right': right}
                    ),
                    content_type='application/json',
                )

                self.assertEqual(response.status_code, 201)
                self.assertEqual(response.json()['result'], expected)

        self.assertEqual(Calculation.objects.count(), len(cases))

    def test_division_by_zero_returns_error_without_saving(self):
        response = self.client.post(
            reverse('calculator:calculate'),
            data=json.dumps({'left': '8', 'operator': '/', 'right': '0'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Cannot divide by zero.')
        self.assertEqual(Calculation.objects.count(), 0)

    def test_invalid_number_returns_error(self):
        response = self.client.post(
            reverse('calculator:calculate'),
            data=json.dumps(
                {'left': '__import__("os")', 'operator': '+', 'right': '1'}
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Calculation.objects.count(), 0)

    def test_invalid_operator_type_returns_error(self):
        response = self.client.post(
            reverse('calculator:calculate'),
            data=json.dumps({'left': '1', 'operator': [], 'right': '2'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Calculation.objects.count(), 0)
