# Gpt 3.5 telegram bot
My unfinished chat-gpt telegram bot

# Architecture
This bot clearly represents a hamburger of different stacks.

Telegram bot is written using python. Data is stored in a separate service written in C# and using Postgres. Services are connected using RabbitMQ. Everything is deployed in docker.
