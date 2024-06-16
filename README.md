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
