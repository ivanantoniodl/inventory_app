# Inventory App

This is a Django project named **inventory_app**. It is designed to manage and track inventory items efficiently.

## Project Structure

The project consists of the following files and directories:

- **inventory_app/**: The main application directory containing the core Django files.
  - **\_\_init\_\_.py**: Indicates that this directory should be treated as a Python package.
  - **asgi.py**: ASGI configuration for the project.
  - **settings.py**: Configuration settings for the Django project.
  - **urls.py**: URL patterns for the project.
  - **wsgi.py**: WSGI configuration for the project.
- **manage.py**: Command-line utility for interacting with the project.
- **requirements.txt**: Lists the Python packages required for the project.
- **README.md**: Documentation for the project.

## Setup Instructions

1. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

## Usage

After starting the development server, you can access the application at `http://127.0.0.1:8000/`.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.