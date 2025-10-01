# Convocore

Convocore is a Django backend API for real time conversations. It is built on Django Rest Framework with WebSockets support. The project supports both one to one conversations and group conversations, making it flexible for chat applications of different scales.

## Features
- User authentication and management
- One to one conversations
- Group conversations
- Real time messaging using WebSockets
- RESTful endpoints for conversation management
- Scalable and extendable architecture

## Tech Stack
- Django
- Django Rest Framework
- Django Channels for WebSockets
- Daphne for channel layer
- SQLite (recommended but can be swapped)

## Installation
1. Clone the repository
```
   git clone https://github.com/eniiifeoluwa/convocore.git
   cd convocore
```
2. Create and activate a virtual environment
```
   python -m venv venv
   source venv/bin/activate   # On Windows use venv\Scripts\activate
```
3. Install dependencies
```
   pip install -r requirements.txt
```
4. Apply migrations
```
   python manage.py migrate
```
5. Run development server
```
   python manage.py runserver
```
6. Run WebSocket worker
   ```
   daphne -b 0.0.0.0 -p 8001 convocore.asgi:application
   ```
## Usage
- Register and authenticate users through REST endpoints
- Create one to one conversations or group conversations
- Send and receive messages in real time via WebSocket connection
- Use REST APIs to list, join or manage conversations

## Example Endpoints
```
- POST /api/register/         -> Register new user
- POST /api/login/            -> Login and receive token
- POST /api/conversations/    -> Create a conversation
- GET  /api/conversations/    -> List user conversations
- POST /api/messages/         -> Send a message
- GET  /api/messages/<id>/    -> Retrieve messages from a conversation
```
## WebSocket
Connect to WebSocket server for live chat:
ws://localhost:8001/ws/chat/<conversation_id>/

## Contributing
Contributions are welcome. Please fork the repository and create a pull request.

## License
This project is licensed under the Apache License.