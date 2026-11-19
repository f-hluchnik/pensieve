# Pensieve

The inspiration for Pensieve comes from the magical object owned by Dumbledore in Harry Potter—a basin used to store and revisit memories. While traditional note-taking apps allow thoughts to be saved, I always felt the need for occasional reminders.

That's where this project began. Slack provided the perfect platform, offering seamless bot integration to make revisiting important thoughts effortless.


## Setup

The detailed description of how to set up and use this project is available on the [Medium](https://medium.com/@f-hluchnik/building-your-own-pensieve-with-slack-dropbox-mongodb-and-python-874adbd41e5d) platform.


# Pensieve: Your Personal Thought Storage System

## Overview
Pensieve is a personal thought storage system that integrates with Slack, MongoDB, and Dropbox. It allows you to send thoughts via Slack, store them in MongoDB, and optionally attach images via Dropbox. Periodic reminders help you revisit your saved thoughts.

## What You Will Need
- **Python**
- **MongoDB** on a static IPv4 address (e.g., via Fly.io) for storing thoughts.
  - *Note:* Fly.io charges for static IPv4 but doesn’t collect fees under $5, effectively making it free.
- **Slack** – used as the interface for Pensieve.
- **Dropbox** (optional) – for storing attachments.
- **NAS/Server with Cron** – to host the Git repository and run scripts for reading and sending messages.

## Setup
### 1. Git Repository
Clone the repository and set up your environment:
```sh
git clone https://github.com/f-hluchnik/pensieve
cd pensieve
python -m venv pensieve_venv
source pensieve_venv/bin/activate
pip install -r requirements.txt
```
Create a `.env` file and populate it with necessary environment variables.

### 2. MongoDB Setup (Fly.io)
1. Install `flyctl`:
   ```sh
   brew install flyctl  # MacOS, or use the appropriate method for your OS
   ```
2. Authenticate:
   ```sh
   flyctl auth login
   ```
3. Initialize the Fly app:
   ```sh
   fly launch --name pensieve-storage --no-deploy
   ```
4. Set secrets:
   ```sh
   fly secrets set MONGO_INITDB_ROOT_USERNAME=<your_username> MONGO_INITDB_ROOT_PASSWORD=<your_password>
   ```
5. Create a volume for persistent storage:
   ```sh
   flyctl volumes create mongodb_data --region <your_region> --size 1
   ```
6. Deploy:
   ```sh
   flyctl deploy
   ```
7. Allocate a dedicated IPv4 address when prompted (*costs $2/month*).
8. Retrieve the connection string:
   ```
   mongodb://<your_username>:<yourpassword>@<app_ipv4_address>:27017
   ```
9. Save the connection string in `.env`:
   ```sh
   MONGO_URI=mongodb://<your_username>:<yourpassword>@<app_ipv4_address>:27017
   DB_NAME=<your_database>
   COLLECTION_NAME=<your_collection>
   ```

### 3. Slack Integration
1. Create a Slack workspace and two channels:
   - `thoughts` (for entering thoughts)
   - `reminders` (for receiving reminders)
2. Retrieve the channel IDs from the Slack URL and add them to `.env`:
   ```sh
   THOUGHTS_CHANNEL_ID=<your_thoughts_channel_id>
   REMINDERS_CHANNEL_ID=<your_reminders_channel_id>
   ```
3. Create a Slack app at [Slack API](https://api.slack.com/apps), and add these **Bot Token Scopes**:
   ```sh
   app_mentions:read, channels:history, chat:write, reminders:write, users:read, files:read, files:write
   ```
4. Install the app and retrieve the **Bot User OAuth Token**. Save it in `.env`:
   ```sh
   SLACK_BOT_TOKEN=<your_bot_token>
   ```
5. Add the app to both Slack channels.

### 4. Dropbox Integration (Optional)
1. Create an app in [Dropbox App Console](https://www.dropbox.com/developers/apps) with **Scoped API Access**.
2. Copy `App Key` and `App Secret` to `.env`:
   ```sh
   APP_KEY=<your_app_key>
   APP_SECRET=<your_app_secret>
   ```
3. Grant permissions: `files.content.write`, `files.content.read`, `sharing.read`, `sharing.write`.
4. Generate an access token:
   ```sh
   chmod +x generate_dropbox_access_code.sh
   ./generate_dropbox_access_code.sh
   ```
5. Follow the script instructions to obtain the refresh token and save it in `.env`:
   ```sh
   DROPBOX_REFRESH_TOKEN=<your_refresh_token>
   ```

## Running the Proof of Concept 🎉
1. Send a message to the `thoughts` channel in Slack.
2. Run the script to read messages:
   ```sh
   python read_messages.py
   ```
3. Verify the new entry in MongoDB (using Compass).
4. Run the script to send reminders:
   ```sh
   python send_message.py
   ```
5. Check the `reminders` channel in Slack.

## Troubleshooting
### SSL Verification Issues
Modify `SlackClient` as follows:
```python
import ssl
import certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())
client = WebClient(token=SLACK_BOT_TOKEN, ssl=ssl_context)
```

## License
This project is licensed under the MIT License.