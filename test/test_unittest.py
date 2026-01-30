"""
Unittest tests for temperature converter
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.temperature_converter import *

class TestTemperatureConverter(unittest.TestCase):

    def test_celsius_to_fahrenheit(self):
        self.assertEqual(celsius_to_fahrenheit(0), 32)
        self.assertEqual(celsius_to_fahrenheit(100), 212)
        self.assertAlmostEqual(celsius_to_fahrenheit(37), 98.6, places=1)

    def test_fahrenheit_to_celsius(self):
        self.assertEqual(fahrenheit_to_celsius(32), 0)
        self.assertEqual(fahrenheit_to_celsius(212), 100)
        self.assertAlmostEqual(fahrenheit_to_celsius(98.6), 37.0, places=1)

    def test_celsius_to_kelvin(self):
        self.assertEqual(celsius_to_kelvin(0), 273.15)
        self.assertEqual(celsius_to_kelvin(100), 373.15)

    def test_kelvin_to_celsius(self):
        self.assertEqual(kelvin_to_celsius(273.15), 0)
        self.assertEqual(kelvin_to_celsius(373.15), 100)

    def test_fahrenheit_to_kelvin(self):
        self.assertAlmostEqual(fahrenheit_to_kelvin(32), 273.15, places=2)
        self.assertAlmostEqual(fahrenheit_to_kelvin(212), 373.15, places=2)

    def test_kelvin_to_fahrenheit(self):
        self.assertAlmostEqual(kelvin_to_fahrenheit(273.15), 32.0, places=1)
        self.assertAlmostEqual(kelvin_to_fahrenheit(373.15), 212.0, places=1)

    def test_is_extreme_temperature(self):
        self.assertTrue(is_extreme_temperature(-50))
        self.assertTrue(is_extreme_temperature(60))
        self.assertFalse(is_extreme_temperature(25))

if __name__ == '__main__':
    unittest.main()