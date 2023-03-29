# Pensieve

The idea of the Pensieve comes from an object owned by Dumbledore in the Harry Potter books. This object, called a pensieve, was used to store memories.
Thoughts can be stored in, for example, an ordinary note-taking application. But I've always thought I'd need to be reminded of them occasionally. That's how the idea for this project came about. Using Slack seemed to be the most feasible way to go, as it is very easy to integrate a bot into Slack.

# Usage

As for now, the project doesn't do much. It just reads the last message from the "thoughts" channel and sends it in the "reminders" channel. In the future, there will be a database for storing your thoughts and some logic which will remind you of random thoughts at random times.

1. Clone this project.
2. Create a one person Slack team.
3. In this team, add two channels - thoughts and reminders.
4. Create an Slack app and install it in this team.
5. Create a `.env` file in the working directory.
6. Add following variables:
  - SLACK_BOT_TOKEN, which is your personal Slack app token
  - THOUGHTS_CHANNEL_ID, which is your thoughts channel id
  - REMINDERS_CHANNEL_ID, which is your reminders channel id
7. Run this script as `python main.py`.
