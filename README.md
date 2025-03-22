# Project Name

## Overview

This project is a web application built using FastAPI, designed to manage various entities such as devices, resellers, services, and users. It leverages SQLAlchemy for database interactions and includes authentication mechanisms using JWT tokens. The project also incorporates Rust-based cryptography libraries for enhanced security.

## Project Structure

- **app**: Contains the core application logic.
  - **database.py**: Manages database connections and sessions.
  - **hashing.py**: Provides password hashing utilities.
  - **models.py**: Defines the database models.
  - **oauth2.py**: Handles OAuth2 authentication.
  - **schemas.py**: Contains Pydantic models for request and response validation.
  - **token.py**: Manages JWT token creation and validation.
  - **repository**: Contains modules for managing data related to devices, resellers, services, and users.
  - **routers**: Contains modules for routing and handling API requests.

- **utils**: Contains utility scripts.
  - **Huawei.py**: Utility script for Huawei-specific tasks.
  - **BDCOM**: Subdirectory for BDCOM-related utilities.

- **__pycache__**: Contains byte-compiled Python files for faster execution.

## Dependencies

The project uses the following main dependencies:
- FastAPI
- Uvicorn
- SQLAlchemy
- Passlib
- Bcrypt
- Python-Jose
- Python-Multipart

Rust-based cryptography libraries are also used, with configurations specified in `Cargo.toml` files located in the `cryptography-x509-verification`, `cryptography-x509`, and `cryptography-openssl` directories.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bistaalish/olt-management-api.git
   cd olt-management-api

2. **Install Python dependencies:**:
```bash
    pip install -r requirements.txt
```
3. **Run the application**:

Use Uvicorn to start the FastAPI application:

```bash
    uvicorn app.main:app --reload
```

## Usage


- Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API exploration.
- Use the available endpoints to manage devices, resellers, services, and users.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details

## Contact

For any questions or support, please contact [bistace321@gmail.com].
