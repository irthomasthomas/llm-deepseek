# llm-deepseek

[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/ghostofpokemon/llm-deepseek?include_prereleases)](https://github.com/ghostofpokemon/llm-deepseek/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ghostofpokemon/llm-deepseek/blob/main/LICENSE)

LLM access to DeepSeek's API

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

```bash
llm install llm-deepseek
```

## Usage

First, set an [API key](https://platform.deepseek.com/api_keys) for DeepSeek:

```bash
llm keys set deepseek
# Paste key here
```

Run `llm models` to list the models, and `llm models --options` to include a list of their options.

Run prompts like this:

```bash
llm -m deepseekchat/deepseek-chat "Describe a futuristic city on Mars"
llm -m deepseekcompletion/deepseek-chat "The AI began to dream, and in its dreams,"
llm -m deepseek-coder "Write a Python function to sort a list of numbers"
llm -m deepseek-coder-completion "Implement a binary search algorithm in Python"
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

```bash
cd llm-deepseek
python3 -m venv venv
source venv/bin/activate
```
