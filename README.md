# Message API Project

This project is a simple **FastAPI** application that allows users to send and retrieve messages, with data stored in an **SQLite** database. The application provides two primary endpoints:

- `POST /send_message/` - Send a message.
- `POST /get_messages/` - Retrieve all messages along with the sender's username and timestamp.

## Features

- **Send a message**: Allows users to send a message along with their username.
- **Get all messages**: Fetches all messages along with the sender's username and timestamp in descending order.
- **SQLite database**: Data is stored in an SQLite database (`messages.db`).

## Requirements

- Python 3.7+
- FastAPI
- SQLite (for database)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/message-api-project.git
   cd message-api-project
