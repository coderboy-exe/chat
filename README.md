# Chattie

Brief description or tagline for your project.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Overview

A simple websocket based chat application powered by django-channels

## Prerequisites

You need to have Docker installed in order to run this application. CHeck out the installagion guide for your Operating System [here](https://www.docker.com/get-started/)

## Installation

Provide step-by-step instructions on how to install and set up your project. Include any configuration steps, environment variables, or database setup required.

```bash
# Clone the repository
git clone https://github.com/yourusername/chattie.git

# Navigate to the project directory
cd chattie

# Install dependencies (for Windows users, open requirements.txt and uncomment this line: # ```twisted-iocpsupport==1.0.4```)
pip install -r requirements.txt

# Perform any additional setup steps (database migrations, etc.)
python manage.py migrate

# Spin up a Redis instance on port 6379 with Docker
docker run --rm -p 6379:6379 redis:7
```

## Usage

Explain how users can run and interact with your project. Include any relevant commands or scripts.

```bash
# Run the development server
python manage.py runserver
```

Access the application at [http://localhost:8000](http://localhost:8000).

## Template Views
```bash
# You can play around with the app in your browser at 127.0.0.1:8000
```
### `GET /api/chat/<str:room_name>/` #### creates a room if it doesnt exist, otherwise, retrieves it


## API Endpoints

### `GET /api/chat/messages/`

Get all messages

### `GET /api/chat/rooms/`

Gets all existing rooms

### `GET /api/chat/rooms/{room_name}/`

Gets details of a particular room.

### `POST /api/chat/mark_as_read/{message_id}/`

Marks a message as "Read"

Refer to the [API documentation](#) for detailed information on each endpoint.

## Contributing

Contributions are highly welcomed.

If you want to contribute to this project, feel free to create a fork, submit an issue, feature request, or pull requests.

## License

This project is free for distribution under the [MIT License](LICENSE).
