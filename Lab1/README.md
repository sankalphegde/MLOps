# Temperature Converter Lab

This project demonstrates a temperature converter with unit tests and CI/CD using GitHub Actions.

## Author
Sankalp Hegde - Northeastern University MLOps Course

## Features
- Convert between Celsius, Fahrenheit, and Kelvin
- Identify extreme temperatures (below -40°C or above 50°C)
- Automated testing with pytest and unittest
- Continuous Integration with GitHub Actions

## Project Structure
```
MLOps/
├── .github/workflows/
├── src/temperature_converter.py
├── test/test_pytest.py
├── test/test_unittest.py
└── requirements.txt
```

## Temperature Conversion Functions

- `celsius_to_fahrenheit(celsius)` - Convert Celsius to Fahrenheit
- `fahrenheit_to_celsius(fahrenheit)` - Convert Fahrenheit to Celsius
- `celsius_to_kelvin(celsius)` - Convert Celsius to Kelvin
- `kelvin_to_celsius(kelvin)` - Convert Kelvin to Celsius
- `fahrenheit_to_kelvin(fahrenheit)` - Convert Fahrenheit to Kelvin
- `kelvin_to_fahrenheit(kelvin)
- `is_extreme_temperature(celsius)` - Check if temperature is extreme

## How to Run Tests
```bash
# Run pytest
python -m pytest test/test_pytest.py -v

# Run unittest
python -m unittest test.test_unittest -v
```

## Modifications from Original Lab

This project differs from the original calculator lab:
- Temperature conversion instead of basic arithmetic
- Extreme temperature detection feature
- Handles three temperature scales with cross-conversions
- Real-world practical application

## Requirements

- Python 3.8+
- pytest
