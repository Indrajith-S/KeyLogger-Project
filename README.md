# Keylogger with Cloud Storage Integration

This Python script captures keylogs and stores them locally, allowing you to send keylog reports via email and upload them to Google Cloud Storage.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project implements a keylogger in Python that captures keystrokes and provides two primary methods of storing and sharing the collected data: sending keylog reports via email and uploading them to Google Cloud Storage.

## Features

- Captures and logs keystrokes.
- Saves keylog reports locally in text files.
- Sends keylog reports via Gmail API.
- Uploads keylog reports to Google Cloud Storage.

## Prerequisites

Before using this project, ensure you have the following prerequisites:

1. Python 3.x installed on your system.
2. Google Cloud project with a valid bucket for Cloud Storage integration.
3. Gmail API credentials (credentials.json) for sending keylog reports via email.

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Indrajith-S/KeyLogger-Project.git
2. Navigate to the project directory:
    ```bash
    cd KeyLogger-Project
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
4. Set up your Google Cloud project:
- Create a Google Cloud project and enable Cloud Storage API.
- Create a Google Cloud Storage bucket and note down its name.
- Download the service account JSON key file (storage.json) and   place it in the project directory.
5. Set up Gmail API:

- Create credentials in the Google Cloud Console and download credentials.json.
- Save credentials.json in the project directory.
6. Run the keylogger script:
    ```bash
    python keylogger.py
7. Press Enter to start capturing keylogs.
8. Press Ctrl + Shift + Backspace to stop capturing.

## Authors

- [@Indrajith S B](https://github.com/Indrajith-S)

