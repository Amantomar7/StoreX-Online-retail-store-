# StoreX Online Retail Store

StoreX is an online retail store project developed using MySQL, Python, Flask, and sklearn. The project aims to provide a functional online retail store with a content-based recommender system.

## Tech Stack

- **Backend**: Python, Flask, MySQL
- **Frontend**: HTML, CSS
- **Machine Learning**: sklearn

## Features

- **User Management**: Create and manage user accounts.
- **Product Catalog**: Browse and search for products.
- **Shopping Cart**: Add, update, and remove items from the cart.
- **Order Management**: Place and view orders.
- **Recommender System**: Content-based recommendations using word vectorization.

## Database Management

The database is managed using the MySQL connector, ensuring efficient handling of user and product data.

## Frontend

The frontend is built using HTML and CSS to create a visually appealing and user-friendly interface.

## Recommender System

The recommender system is content-based, analyzing customer history to suggest relevant products. It leverages word vectorization techniques to provide accurate recommendations.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/StoreX.git
   cd StoreX
   ```

2. Set up the virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure the MySQL database:
   - Ensure MySQL is installed and running.
   - Create a new database and update the connection details in the configuration file.

4. Run the application:
   ```bash
   flask run
   ```

5. Access the application at `http://localhost:5000`.

## Usage

1. Register or log in to your account.
2. Browse the product catalog and add items to your cart.
3. Place an order and view order history.
4. Receive product recommendations based on your browsing and purchase history.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Thanks to the contributors of Flask, sklearn, and other open-source libraries used in this project.

---
