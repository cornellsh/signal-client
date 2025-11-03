# Writing Asynchronous Commands

The `signal-client` library is built on `asyncio` to handle a large number of concurrent operations efficiently. The performance of this model depends entirely on **never blocking the event loop**. A single blocking I/O call in a command can freeze a worker, reduce the overall throughput of the bot, and lead to a poor user experience.

This document provides essential guidelines for writing high-performance, non-blocking commands.

## The Golden Rule: Never Block the Event Loop

An `async` function must never perform a blocking operation. This includes:

- **Synchronous HTTP Requests:** Using libraries like `requests`.
- **Standard File I/O:** Using `open()`, `file.read()`, or `file.write()`.
- **CPU-Intensive Operations:** Long-running calculations that can hog the CPU.
- **Calling `time.sleep()`:** This will put the entire worker to sleep.

## Asynchronous Alternatives

Always use the asynchronous equivalent for any I/O-bound operation.

| Operation         | Forbidden (Blocking)     | Recommended (Asynchronous)                          |
| ----------------- | ------------------------ | --------------------------------------------------- |
| **HTTP Requests** | `requests.get()`         | `context.session.get()` (via the `aiohttp` session) |
| **File I/O**      | `open()`, `pathlib.Path` | `aiofiles`                                          |
| **Sleeping**      | `time.sleep()`           | `asyncio.sleep()`                                   |
| **Database**      | `sqlite3`, `psycopg2`    | `aiosqlite`, `asyncpg`                              |
| **Subprocesses**  | `subprocess.run()`       | `asyncio.create_subprocess_exec()`                  |

### Example: Fetching Data from an API

**Incorrect (Blocking):**

```python
import requests

async def handle(self, context: Context) -> None:
    # This will block the worker!
    response = requests.get("https://api.example.com/data")
    await context.send(response.text)
```

**Correct (Asynchronous):**

```python
async def handle(self, context: Context) -> None:
    # This is non-blocking and safe to use.
    async with context.session.get("https://api.example.com/data") as response:
        text = await response.text()
        await context.send(text)
```

## Handling CPU-Bound Work

If you have a command that needs to perform a CPU-intensive calculation, you must run it in a separate thread or process to avoid blocking the event loop. The recommended way to do this is with `asyncio.to_thread()` (Python 3.9+).

**Correct (Offloading to a Thread):**

```python
import asyncio

def blocking_cpu_intensive_function():
    # Simulate a long-running calculation
    # ...
    return "some result"

async def handle(self, context: Context) -> None:
    # Offload the blocking function to a separate thread
    result = await asyncio.to_thread(blocking_cpu_intensive_function)
    await context.send(result)
```

By following these guidelines, you will help to ensure that the bot remains fast, responsive, and stable, even under heavy load.
