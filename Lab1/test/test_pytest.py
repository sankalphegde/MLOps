"""
Pytest tests for temperature converter
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.temperature_converter import *

def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(0) == 32
    assert celsius_to_fahrenheit(100) == 212
    assert round(celsius_to_fahrenheit(37), 1) == 98.6

def test_fahrenheit_to_celsius():
    assert fahrenheit_to_celsius(32) == 0
    assert fahrenheit_to_celsius(212) == 100
    assert round(fahrenheit_to_celsius(98.6), 1) == 37.0

def test_celsius_to_kelvin():
    assert celsius_to_kelvin(0) == 273.15
    assert celsius_to_kelvin(-273.15) == 0
    assert celsius_to_kelvin(100) == 373.15

def test_kelvin_to_celsius():
    assert kelvin_to_celsius(273.15) == 0
    assert kelvin_to_celsius(373.15) == 100
    assert kelvin_to_celsius(0) == -273.15

def test_fahrenheit_to_kelvin():
    assert round(fahrenheit_to_kelvin(32), 2) == 273.15
    assert round(fahrenheit_to_kelvin(212), 2) == 373.15

def test_kelvin_to_fahrenheit():
    assert round(kelvin_to_fahrenheit(273.15), 1) == 32.0
    assert round(kelvin_to_fahrenheit(373.15), 1) == 212.0

def test_is_extreme_temperature():
    assert is_extreme_temperature(-50) == True
    assert is_extreme_temperature(60) == True
    assert is_extreme_temperature(25) == False