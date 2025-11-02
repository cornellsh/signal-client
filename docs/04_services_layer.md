# Services Layer

The `services` layer contains the core application logic of the `signal-client` library. These services are responsible for orchestrating the flow of data and coordinating the interactions between the low-level infrastructure (like the WebSocket client and API client) and the high-level command processing.

### `command_service.py`

- **Purpose:** This is one of the most critical services in the library. Its primary responsibility is to consume messages from the central `MessageQueue`. For each message, it iterates through all registered commands and checks if the message content matches any of the command's `triggers`. If a match is found, it instantiates a `Context` object for the message and executes the command's `handle` method.

### `message_service.py`

- **Purpose:** This service is responsible for the "listening" part of the bot. It uses the `WebSocketClient` from the infrastructure layer to listen for incoming messages from the Signal service. When a new message is received, the `MessageService`'s job is to place it into the `MessageQueue`, where it can be picked up by the `CommandService` for processing.

### `storage_service.py`

- **Purpose:** This service provides an abstraction for persistent storage. It allows the bot to store and retrieve data, which can be used for various purposes such as remembering user preferences, storing session information, or caching data. The actual storage mechanism (e.g., Redis, SQLite) is managed in the `infrastructure/storage` directory, allowing the service to remain agnostic to the implementation details.
