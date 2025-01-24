# Cognito Demo with FastAPI

This is a demo application that demonstrates how to integrate AWS Cognito authentication with a FastAPI application using Authlib.

## Setup

### Prerequisites

- Python 3.7+
- AWS Cognito User Pool
- AWS Cognito App Client with allowed callback URLs configured

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/cognito_demo.git
    cd cognito_demo
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. Update the `client_secret` in `main.py` with your Cognito App Client secret.

### Running the Application

1. Start the FastAPI application:
    ```bash
    uvicorn main:app --host localhost --port 8000
    ```

2. Open your browser and navigate to `http://127.0.0.1:8000`.

## Application Routes

- `/` - Home route that checks the session for a logged-in user.
- `/login` - Login route that redirects the user to Cognito for authentication.
- `/authorize` - Callback route that Cognito redirects to after authentication.
- `/logout` - Logout route that removes the user from the session.

## License

This project is licensed under the MIT License.

