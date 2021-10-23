import praw
from prawcore.exceptions import Forbidden
import requests
import time

USER_AGENT = "Reddit Comment/Post Deleter by Subreddit Bot v1.1 by /u/PMDev123"

# Fill in your Reddit account information
USERNAME = ""
PASSWORD = ""
CLIENT_ID = ""
CLIENT_SECRET = ""

# Subreddits to delete comments/posts from
# For multiple subreddits, format it like: ["sub1", "sub2", "sub3"]
SUBREDDITS = ["x"]

# Delete comments OLDER than this number of days (not inclusive)
# If you want to delete EVERYTHING from the subreddit, set it to 0
# If you want to do this from multiple subreddits with DIFFERENT timer values, put the subreddits individually
TIMER = 0


def get_comment_body_list():
    # Get all of the user's comments from the subreddit and store the ID & body
    # Based on u/shiruken's code snippet: https://www.reddit.com/r/pushshift/comments/bfc2m1/capping_at_1000_posts/
    last = 0
    id_list = []
    body_list = []

    for sub in SUBREDDITS:
        url = f'https://api.pushshift.io/reddit/search/comment/?author={USERNAME}&subreddit={sub}&fields=id,created_utc,body&before={TIMER}d'
        print("Getting comment IDs for user " + USERNAME + " from /r/" + sub +
              " older than " + str(TIMER) + " days. Please wait:")
        N = 0
        while N < 10000:
            if N == 0:
                request = requests.get(url)
                # Avoid rate limiting
                time.sleep(1)
                json = request.json()
            else:
                # Make a new request for comments before the one stored in 'last'
                new_url = f"https://api.pushshift.io/reddit/search/comment/?author={USERNAME}&subreddit={sub}&fields=id,created_utc,body&before={last}"
                request = requests.get(new_url)
                time.sleep(1)
                json = request.json()
            if not json.get("data"):
                # No more results
                break
            for s in json['data']:
                # Add the comment id and body to separate lists
                id_list.append(s['id'])
                body_list.append(s['body'])
                N += 1
            # 'last' is the last comment's created_utc variable in the JSON
            last = int(s['created_utc'])
        print(N, "comments detected from /r/" + sub + ".")

    return id_list, body_list


def get_post_body_list():
    # Get all of the user's posts from the subreddit and store the ID & body
    # Based on u/shiruken's code snippet: https://www.reddit.com/r/pushshift/comments/bfc2m1/capping_at_1000_posts/
    last = 0
    id_list = []
    title_list = []

    for sub in SUBREDDITS:
        print("Getting post IDs for user " + USERNAME + " from /r/" + sub +
              " older than " + str(TIMER) + " days. Please wait:")
        url = f'https://api.pushshift.io/reddit/search/submission/?author={USERNAME}&subreddit={sub}&fields=id,created_utc,title&before={TIMER}d'

        N = 0
        while N < 10000:
            if N == 0:
                request = requests.get(url)
                # Avoid rate limiting
                time.sleep(1)
                json = request.json()
            else:
                # Make a new request for posts before the one stored in 'last'
                new_url = f"https://api.pushshift.io/reddit/search/submission/?author={USERNAME}&subreddit={sub}&fields=id,created_utc,title&before={last}"
                request = requests.get(new_url)
                time.sleep(1)
                json = request.json()
            if not json.get("data"):
                # No more results
                break
            for s in json['data']:
                # Add the post id and body to separate lists
                id_list.append(s['id'])
                title_list.append(s['title'])
                N += 1
            # 'last' is the last post's created_utc variable in the JSON
            last = int(s['created_utc'])
        print(N, "comments detected from /r/" + sub + ".")

    return id_list, title_list


def delete_all_comments(reddit, id_list, body_list):
    # Delete all the comments that were detected in the subreddit
    count = 0
    try:
        reddit.validate_on_submit = True
        # Loop over list of comments
        for i in range(len(id_list)):
            comment = reddit.comment(id_list[i])
            try:
                # Edit/overwrite the comment before deleting. Comment out the next three lines if you don't want to.
                comment.edit("Lorem ipsum")
                time.sleep(1)
                print("Edited comment", id_list[i], "with body:", body_list[i])

                # Delete the comment
                comment.delete()
                time.sleep(1)
                print("Deleted comment", id_list[i], "with body:", body_list[i])

                count += 1
            except Forbidden:
                # Case where you try to edit a post that's already deleted
                print("Comment", id_list[i], "already deleted. Skipping...")
    except IndexError:
        print("There was an error trying to delete comments. The subreddit might be private.")

    print("")
    print("Deleted " + str(count) + " comments in total.")


def delete_all_posts(reddit, id_list, body_list):
    # Delete all the posts that were detected in the subreddit
    count = 0
    try:
        reddit.validate_on_submit = True
        # Loop over list of posts
        for i in range(len(id_list)):
            submission = reddit.submission(id_list[i])

            # Delete the post
            submission.delete()
            time.sleep(1)
            print("Deleted post", id_list[i], "with body:", body_list[i])

            count += 1
    except IndexError:
        print("There was an error trying to delete comments. The subreddit might be private.")

    print("")
    print("Deleted " + str(count) + " posts in total.")


if __name__ == "__main__":
    start = time.time()

    comment_id_list, comment_body_list = get_comment_body_list()
    print()
    print("Comment IDs returned.")
    print()

    post_id_list, post_body_list = get_post_body_list()
    print()
    print("Post IDs returned.")
    print()

    print("Logging in: ")
    redditLogin = praw.Reddit(
        username=USERNAME,
        password=PASSWORD,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )
    print("Login successful.")
    print()

    print("Deleting comments:")
    delete_all_comments(redditLogin, comment_id_list, comment_body_list)
    print()

    print("Deleting posts:")
    delete_all_posts(redditLogin, post_id_list, post_body_list)
    print()

    end = time.time()
    print("Time taken to run:", round(end - start, 2), "seconds")
    print("Done!")
    