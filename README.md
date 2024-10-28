# Supermarket Price Comparison 

A Django-based web application that allows users to compare product prices across different shops. 

## Features

- **Shop Selection and Price Comparison**: Allows users to search and select products by barcode and displays prices from various shops.
- **Dynamic Price Updates**: Newly entered products automatically append to the comparison table for easy viewing.
- **Receipt-Like Interface**: Displays price comparisons in a "supermarket receipt" style, enhancing readability.

## Prerequisites

- **Python 3.7+**
- **Poetry** for dependency management

## Installation

To get started with the project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/supermarket-price-comparison.git
    cd supermarket-price-comparison
    ```

2. **Install Dependencies with Poetry**:
   Ensure you have [Poetry installed](https://python-poetry.org/docs/#installation) on your system.
   ```bash
   poetry install

3. **Set Up Environment Variables**: 
    Create a .env file in the root directory and add your settings:
    ```bash
    DEBUG=True

4. **Run migrations**: 
    ```bash
    poetry run python manage.py migrate

5. **Run the server**: 
    ```bash
    poetry run python manage.py runserver

6. **access the appliaction**:
    Open your web browser and go to `http://127.0.0.1:8000/`

## Usage

1. Enter shop indentifiers : On the homepage, enter the shops ID to retrieve its price data for all the available products (currently two shops can be compared)
2. Compare Prices: The application will display a table with products on each row and shops in columns that allow you to compare the price for each product and for the total of the products available.

## Data Source

This application utilizes pricing data from the Open Prices project (Open Food Facts).

## Acknowledgments

Special thanks to [Open Prices](https://prices.openfoodfacts.org/) for providing the open product data used in this project.