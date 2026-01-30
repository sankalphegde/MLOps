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
├── .github/
│   └── workflows/
│       ├── pytest_action.yml
│       └── unittest_action.yml
├── src/
│   ├── __init__.py
│   └── temperature_converter.py
├── test/
│   ├── __init__.py
│   ├── test_pytest.py
│   └── test_unittest.py
├── data/
│   └── __init__.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Temperature Conversion Functions

- `celsius_to_fahrenheit(celsius)` - Convert Celsius to Fahrenheit
- `fahrenheit_to_celsius(fahrenheit)` - Convert Fahrenheit to Celsius
- `celsius_to_kelvin(celsius)` - Convert Celsius to Kelvin
- `kelvin_to_celsius(kelvin)` - Convert Kelvin to Celsius
- `fahrenheit_to_kelvin(fahrenheit)` - Convert Fahrenheit to Kelvin
- `kelvin_to_fahrenheit(kelvin)` - Convert Kelvin to Fahrenheit
- `is_extreme_temperature(celsius)` - Check if temperature is extreme

## How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/MLOps.git
cd MLOps
```

### 2. Create and activate virtual environment
```bash
python -m venv MLOps_env
source MLOps_env/bin/activate  # On Windows: MLOps_env\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run tests

**Run pytest:**
```bash
python -m pytest test/test_pytest.py -v
```

**Run unittest:**
```bash
python -m unittest test.test_unittest -v
```

## GitHub Actions CI/CD

This repository uses GitHub Actions for continuous integration. Every push to the `main` branch automatically:
1. Runs pytest tests
2. Runs unittest tests
3. Reports test results

You can view the test results in the "Actions" tab of the GitHub repository.

## Example Usage
```python
from src.temperature_converter import *

# Convert 100°C to Fahrenheit
temp_f = celsius_to_fahrenheit(100)
print(f"100°C = {temp_f}°F")  # Output: 100°C = 212.0°F

# Check if temperature is extreme
is_extreme = is_extreme_temperature(-50)
print(f"Is -50°C extreme? {is_extreme}")  # Output: True
```

## Modifications from Original Lab

This project differs from the original calculator lab in the following ways:
- **Different functionality**: Temperature conversion instead of basic arithmetic
- **Additional feature**: Extreme temperature detection
- **More complex conversions**: Handles three temperature scales with cross-conversions
- **Real-world application**: Practical use case for temperature conversion

## Requirements

- Python 3.8+
- pytest
- unittest (built-in)

## License

This project is created for educational purposes as part of the MLOps course at Northeastern University.
```

---

## **STEP 2: Update requirements.txt**

Make sure your `requirements.txt` contains:
```
pytest
```

---

## **STEP 3: Update .gitignore**

Make sure your `.gitignore` contains:
```
# Virtual Environment
MLOps_env/
venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db