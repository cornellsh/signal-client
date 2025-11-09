---
title: What Signal Client Can Do
summary: Core features for building Signal bots.
order: 3
---

## Core features

### Messaging
- **Send messages** - Text, media, reactions to individuals or groups
- **Receive messages** - Handle incoming messages with command triggers
- **Attachments** - Send images, files, and other media
- **Group support** - Work with Signal groups and private chats

### Command system
- **Trigger patterns** - Respond to specific text patterns or commands
- **Context handling** - Access message sender, group info, and content
- **Async support** - Handle multiple messages concurrently
- **Error handling** - Built-in retry and error recovery

### Bot management
- **Device linking** - Connect your bot to Signal via QR code
- **Configuration** - Simple config file or environment variables
- **Logging** - Track what your bot is doing
- **Persistence** - Store data between restarts

## What you can build

- **Command bots** - Respond to `!weather`, `!joke`, `!help` etc.
- **Notification bots** - Get alerts from your servers or services
- **Group moderators** - Auto-welcome, enforce rules, manage spam
- **Personal assistants** - Reminders, shopping lists, family coordination
- **Integration bots** - Connect Signal to other services you use

## Getting started

1. **Install** - `pip install signal-client`
2. **Setup signal-cli-rest-api** - The backend service that connects to Signal
3. **Link your device** - Scan QR code to connect your bot
4. **Write commands** - Use `@command("!hello")` decorators
5. **Run your bot** - Start listening for messages

!!! tip "Start simple"
    Begin with a basic ping/pong bot, then add features as you learn. Signal bots work best when they solve specific problems for your group or personal use.

> **Next step** · Follow our [Quickstart](quickstart.md) guide to build your first bot.
