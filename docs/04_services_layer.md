# Services Layer

The `services` layer contains the core application logic of the `signal-client` library. These services are responsible for orchestrating the flow of data and coordinating the interactions between the low-level infrastructure and the high-level command processing.

### `worker_pool_manager.py`

- **Purpose:** This is the heart of the message processing engine. It creates and manages a pool of `Worker` tasks. This provides bounded concurrency, ensuring the system remains stable under heavy load. The manager is also responsible for registering commands and distributing them to the workers.

### `message_service.py`

- **Purpose:** This service is responsible for the "listening" part of the bot. It uses the `WebSocketClient` from the infrastructure layer to listen for incoming messages from the Signal service. When a new message is received, the `MessageService`'s job is to place it into the `MessageQueue`, where it can be picked up by a `Worker` for processing.
