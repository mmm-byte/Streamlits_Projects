# Streamlit Project

This repository contains all the necessary files to deploy a Streamlit application. This project securely handles Google credentials using Streamlit's secrets management system to interact with Google Sheets and Google Drive.

## Overview

This Streamlit application allows users to submit responses that are stored in a Google Sheet. The app is deployed on Streamlit Cloud, and Google credentials are securely managed using the Streamlit secrets management system.

## Files

- `main.py`: The main Streamlit application file.
- `.streamlit/secrets.toml`: Contains the Google credentials in TOML format.

## Prerequisites

Ensure you have the following installed:

- Python 3.7 or higher
- Streamlit
- Google API Client Libraries (`google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, `gspread`, `pydrive`)

You can install the necessary Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Setup

### 1. Clone the repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/mmm-byte/Streamlits_Projects/tree/3c13a1bbdee8000a18e7af1e64cd65a9fd2f90b5/Feedback_Chatbot
cd your-repository
```

### 2. Add Google Credentials

To securely handle your Google credentials, use the Streamlit secrets management system. Convert your `credentials.json` to a TOML format and add it to the Streamlit secrets file.

Example `secrets.toml`:

```toml
[GOOGLE_CREDENTIALS]
type = "service_account"
project_id = "your-project-id"
```

### 3. Deploying on Streamlit Cloud

1. **Go to Your Streamlit Cloud Workspace**: Open [Streamlit Cloud](https://share.streamlit.io/).
2. **Select Your Application**: Navigate to the app you want to deploy.
3. **Go to the Settings of Your Application**:
   - Click on the app you want to configure.
   - Click on the "Settings" icon (⚙️).
4. **Add Secrets**:
   - In the "Secrets" section, add your secrets as key-value pairs.
   - Add a secret with the key `GOOGLE_CREDENTIALS` and paste the TOML content of your credentials as the value.
5. **Save and Deploy**: Save your changes and deploy your app.

### 4. Running Locally

If you want to run the app locally for testing purposes, follow these steps:

1. Set the environment variables for Google credentials:

```bash
export GOOGLE_CREDENTIALS='{
  "type": "service_account",
  "project_id": "your-project-id",
}'
```

2. Run the Streamlit app:

```bash
streamlit run main.py
```

This README file provides a clear and concise setup process for your Streamlit application.

