# Exchange Project

## Getting Started

### Prerequisites
- Python 3.12+
- Docker and Docker Compose
- PostgreSQL
- Git

### Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone https://github.com/sudoAlireza/exchange.git
    cd exchange
    ```

2. **Create a `.env` file**:
    Copy the `env.sample` file to `.env` and customize the environment variables as needed:
    ```bash
    cp env.sample .env
    ```

3. **Run the project using Docker**:
    Build and run the services:
    ```bash
    docker compose up --build
    ```

4. **Load initial data**:
    Run the following command to load fixture data (currencies):
    ```bash
    docker compose exec web python manage.py loaddata fixtures/currencies.json
    ```

5. **Create a superuser**:
    To access the Django admin, create a superuser:
    ```bash
    docker compose exec web python manage.py createsuperuser
    ```

6. **Access the application**:
    The app will be available at `http://localhost:8000`.



## API Documentation

- **Swagger**: Visit `http://localhost:8000/api/schema/swagger-ui/` to view the swagger API documentation.


## Deployment

For production:
- USE `APP_ENV = PRODUCTION`
- Configure allowed hosts (`ALLOWED_HOSTS`)
