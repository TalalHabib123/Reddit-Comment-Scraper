import praw

client_id = 'YourClientID'
client_secret = 'YourSecret'
user_agent = 'YourAgent'
refresh_token = 'YourRefershToken'

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    refresh_token=refresh_token
)