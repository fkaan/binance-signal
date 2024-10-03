# Binance Divergence Detection with Telegram Alerts

This project identifies bullish and bearish RSI divergences across all Binance futures trading pairs and sends alerts to a specified Telegram chat. The script continuously checks for divergences and sends real-time notifications via Telegram when a signal is detected.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)

## Introduction

The **Binance Divergence Detection** script uses the Binance API to pull price data for all futures trading pairs. It calculates the Relative Strength Index (RSI) using the `ta` library and checks for divergences. Upon detecting a bullish or bearish divergence, the script sends a notification to a specified Telegram chat using a bot.

## Features

- Fetches real-time market data for all Binance futures trading pairs.
- Calculates the RSI for each pair using the `ta` library.
- Detects bullish and bearish divergences based on price action and RSI values.
- Sends real-time notifications to a Telegram chat when a divergence is detected.
  
## Installation

To run this project, you'll need to install the necessary Python libraries:

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/binance-divergence-telegram.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `config.py` file in the root directory and add your Binance API key and secret:

    ```python
    key = 'your_binance_api_key'
    secret = 'your_binance_api_secret'
    ```

## Configuration

1. **Telegram Bot Setup:**

    - Create a bot via the [BotFather](https://core.telegram.org/bots#botfather) and get the token.
    - Get your `chat_id` by sending a message to your bot and visiting the following URL in your browser:

        ```
        https://api.telegram.org/bot<your-bot-token>/getUpdates
        ```

    - The `chat_id` can be found in the message JSON.

2. **Add Telegram Bot Information:**

    Update the following variables in your script with your bot's token and chat ID:

    ```python
    token = 'your_telegram_bot_token'
    chat_id = 'your_telegram_chat_id'
    ```

## Usage

Once everything is set up, run the script to continuously monitor for divergences:

```bash
python divergence_detection.py
```
The script will:

- Retrieve real-time futures market data from Binance.
- Calculate the RSI for each trading pair.
- Identify bullish or bearish divergences.
- Send an alert to your Telegram chat with the signal.

### Example of a Telegram Alert

- **Bullish Divergence**:
    ```
    BTCUSDT RSI: 29.87
    Pozitif Uyumsuzluk Sinyali. 🟢
    ```

- **Bearish Divergence**:
    ```
    BTCUSDT RSI: 71.23
    Negatif Uyumsuzluk Sinyali. 🔴
    ```


