from RedditCredentials import reddit
import pandas as pd
from tqdm import tqdm
import time

def save_posts_to_csv(posts):
    csv_filename = 'Controversial_Posts.csv'
    df = pd.DataFrame(posts)
    df.to_csv(csv_filename, index=False, mode='a', header=False)
    
def load_processed_subreddits():
    try:
        with open('processed_subreddits.csv', 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

def save_processed_subreddit(subreddit_name):
    with open('processed_subreddits.csv', mode='a', newline='') as file:
        file.write(subreddit_name+'\n')

def get_most_controversial_posts(subreddit_list, limit_per_subreddit=5):
    processed_subreddits = load_processed_subreddits()
    for subreddit_name in tqdm(subreddit_list, desc="Subreddits", unit="subreddit"):
        if subreddit_name in processed_subreddits:
            print(f"Skipping subreddit '{subreddit_name}' as it has already been processed.")
            continue
        subreddit = reddit.subreddit(subreddit_name)
        for post in tqdm(subreddit.controversial(limit=limit_per_subreddit, time_filter='all'), desc=f"{subreddit_name} Posts", unit="post"):
            print(post.title)
            comments_data = []
            try:
                post.comments.replace_more(limit=None, threshold=0)  # Set threshold to 0 to get all comments
            except Exception as e:
                print(f"Error: Unable to retrieve all comments for post '{post.title}' - {e}")
                continue
            for comment in tqdm(post.comments.list(), desc="Comments", unit="comment"):
                if comment.body and comment.author:
                    author_name = comment.author.name if comment.author else "Unknown"
                    comment_data = {
                        'Post_Title': post.title,
                        'Comment_Text': comment.body,
                        'Comment_Author': author_name,
                        'Label': None
                    }
                    comments_data.append(comment_data)
            save_comments_to_csv(comments_data)
            time.sleep(0.5)
        save_processed_subreddit(subreddit_name)
        time.sleep(1)

def save_comments_to_csv(comments_data):
    df = pd.DataFrame(comments_data)
    df.to_csv('reddit_comments.csv', mode='a', index=False, header=True)

if __name__ == "__main__":
    subreddit_list = pd.read_csv('subreddit_data.csv')

    limit_per_subreddit = 5

    get_most_controversial_posts(subreddit_list, limit_per_subreddit)