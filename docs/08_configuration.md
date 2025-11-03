# Configuration Reference

The `signal-client` library is configured via a Python dictionary passed to the `SignalClient` constructor. This document details all the available configuration options.

---

## Core Configuration

These are the essential settings required to get your bot running.

### `signal_service`

- **Type:** `str`
- **Description:** The URL of the `signal-cli-rest-api` service.
- **Example:** `"localhost:8080"`

### `phone_number`

- **Type:** `str`
- **Description:** The phone number of your bot's Signal account, in E.164 format.
- **Example:** `"+1234567890"`

---

## Performance Tuning

These settings allow you to fine-tune the performance of your bot.

### `worker_pool_size`

- **Type:** `int`
- **Default:** `4`
- **Description:** The number of concurrent worker tasks that will be created to process incoming messages. A larger pool size can handle a higher volume of messages but will consume more system resources.
- **Example:** `8`

---

## Example Configuration

Here is an example of a complete configuration dictionary:

```python
config = {
    "signal_service": "localhost:8080",
    "phone_number": "+1234567890",
    "worker_pool_size": 8,
}

client = SignalClient(config)
```
