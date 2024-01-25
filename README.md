# Chattie

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Overview

A simple websocket based chat application powered by django-channels and Redis

## Prerequisites

You need to have Docker installed in order to run this application. CHeck out the installagion guide for your Operating System [here](https://www.docker.com/get-started/)

## Installation

### Method 1
```bash
# Simply pull the image 
docker pull coderboyexe/chat-chattie:latest
```

### Method 2
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

Simply run the dev server

```bash
# Run the development server
python manage.py runserver
```

Access the application at [http://localhost:8000](http://localhost:8000).

Note: You can change the default API_KEY value provided in `settings.py`, the default value is `my_api_key`

## Template Views

### In your browser:

### `loccalhost:8000/api/chat/<str:room_name>?api_key=my_api_key`
Creates a room if it doesnt exist, otherwise, retrieves it

## Testing

```bash
# Run the tests
python manage.py test
```
All tests shoud pass

## API Endpoints

#### `GET /api/chat/messages/?api_key=my_api_key`

Gets all messages

#### `GET /api/chat/messages/?api_key=my_api_key?room_id=<int:room_id>`

Gets all messages in a specific room (id)

#### `GET /api/chat/rooms?api_key=my_api_key`

Gets all existing rooms

#### `GET /api/chat/rooms/{room_name}?api_key=my_api_key`

Gets details of a particular room.

#### `POST /api/chat/mark_as_read/{message_id}?api_key=my_api_key`

Marks a message as "Read"

Refer to the [API documentation](#) for detailed information on each endpoint.

## Contributing

Contributions are highly welcomed.

If you want to contribute to this project, feel free to create a fork, submit an issue, feature request, or pull requests.

## License

This project is free for distribution under the [MIT License](#license).
