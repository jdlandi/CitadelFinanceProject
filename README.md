# Citadel Finance Project

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [In-Depth Feature Breakdown](#in-depth-feature-breakdown)
- [Technical Architecture](#technical-architecture)
- [Project Structure](#project-structure)
- [Development Process](#development-process)
- [Code Explanation](#code-explanation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## Overview

Citadel Finance is a cutting-edge web application designed to provide users with a comprehensive suite of financial tools and services. Whether you're a seasoned investor or just starting your financial journey, Citadel Finance offers a range of features to help you make informed decisions and stay ahead of the market.

## Features

1. **User Authentication**: Secure sign-up and login functionality with input verification and password hashing.
2. **Flashcards**: Generate AI-powered flashcards for learning and information retention.
3. **Portfolio Management**: Manage and track stock portfolios with insights into holdings and performance.
4. **News**: Search for news articles based on specific queries and get AI-powered summaries.
5. **Forex Trading**: Get insights into forex trading with exchange rates and trading pairs.
6. **AI Assistance**: Leverage AI models for flashcards, news summarization, and more.

## In-Depth Feature Breakdown

- **AI-Powered Flashcards**: Citadel Finance uses OpenAI models to generate insightful flashcards based on user queries. This feature allows users to learn about financial concepts, stock analysis, forex trading, and more in an interactive and engaging way.
- **Portfolio Management**: Users can create and manage multiple stock portfolios, track their holdings, and view performance metrics. The application provides real-time data on stock prices, price differences, daily highs and lows, and more.
- **News Summarization**: Users can search for news articles on specific topics and get AI-powered summaries. This feature helps users stay updated on market trends, company news, and financial developments without spending hours reading articles.
- **Forex Trading Insights**: Citadel Finance offers insights into forex trading by providing exchange rates, profitable trading pairs, and potential profit calculations. Users can explore different currency pairs and make informed trading decisions.

## Technical Architecture

Citadel Finance is built on the Flask web application framework for Python. The backend is powered by Python, and the frontend is developed using HTML, CSS, and JavaScript. The application uses MongoDB for data storage and OpenAI models for AI-powered assistance. Various APIs are used to retrieve news articles and forex trading data.

## Project Structure

- **`app.py`**: Main Flask application, handles routing, user authentication, and web page rendering.
- **`datatypes.py`**: Defines custom data types and utility functions for stocks, forex, flashcards, and more.
- **`model.py`**: Contains functions related to AI models and APIs for news and financial data.
- **`/templates`**: Contains HTML templates for rendering web pages.
- **`/static`**: Contains static assets such as CSS stylesheets and images.

## Development Process

The development of Citadel Finance followed an iterative and agile approach. The project began with a thorough planning phase, during which the features, technical architecture, and design were finalized. The development process was divided into several sprints, with each sprint focused on a specific set of features or improvements.

During each sprint, the code was developed, tested, and integrated into the main codebase. Continuous integration and continuous deployment (CI/CD) practices were followed to ensure that the application remained stable and functional throughout the development process.

The application underwent rigorous testing, including unit testing, integration testing, and user acceptance testing (UAT). Feedback from UAT was used to further refine and optimize the application.

## Code Explanation

- **User Authentication**: Citadel Finance uses a secure authentication system that includes input verification, password hashing, and cookie management. User passwords are hashed using the SHA-256 algorithm for added security. The `input_verification` function ensures that usernames and passwords meet specific criteria, such as minimum length.
- **Flashcards Generation**: The `flashcards` and `save_flashcards` routes in `app.py` handle flashcard generation and saving. The `ask_ai` function in `model.py` uses OpenAI models to generate flashcards based on user queries.
- **Portfolio Management**: The `portfolio` route in `app.py` allows users to manage their stock portfolios. The `gen_stock` function in `datatypes.py` generates stock data, including ticker, original price, current price, price difference, and daily highs and lows.
- **News Summarization**: The `news` route in `app.py` handles news article searches and summarization. The `get_search` function in `model.py` retrieves news articles based on user queries and provides summaries using AI models.
- **Forex Trading Insights**: The `currency` route in `app.py` provides forex trading insights. The `calculate_forex` function in `datatypes.py` calculates potential profits for different currency pairs based on exchange rates.

## Usage

This repository showcases the code powering the live version of Citadel Finance. It is not intended for local deployment. Visit the live version at [www.startcitadel.com](https://www.startcitadel.com).

## Technologies Used

- **Flask**: Web application framework for Python.
- **OpenAI**: AI models for flashcards and assistance.
- **NewsAPI**: API for news articles.
- **ExchangeRate.host**: API for forex data.
- **MongoDB**: Database for data storage.
- **HTML/CSS/JavaScript**: Frontend development.

## Contributing

While this project is primarily a showcase, contributions are welcome. Submit a pull request or open an issue for suggestions or improvements.

## Authors

[Jay Landi](https://www.linkedin.com/in/jdlandi/) | California Institute of Technology

[Lucia Wang](https://www.linkedin.com/in/lucia-wang-a3a58b248/) | Massachusetts Institute of Technology


## License

This project is licensed under the MIT License.
