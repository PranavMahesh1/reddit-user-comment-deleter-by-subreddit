# Reddit User Comment/Post Deleter By Subreddit

This is a Python script I made for **deleting all of your Reddit comments and posts from a specific subreddit**. Many existing tools online use Reddit's API to do this, however Reddit only fetches your last 1000 comments/posts due to API limitations, which can miss many comments. This script uses the [Pushshift API](https://github.com/pushshift/api) to bypass this limit and to be able to return more than 1000 comments/posts.

If you would like to see what posts are returned, use [this tool](https://camas.github.io/reddit-search/) to search for your comments or posts by subreddit.

## Setup

You will need **Python 3.6** or a higher version in order to run this script. This script was tested with Python 3.9.

### Installation (Windows)
When Python is installed, type these commands in command prompt:

    py 3 -m pip install praw
    py 3 -m pip install prawcore
    py 3 -m pip install requests


### Installation (OS X/Linux)
Run if pip is not installed:

    sudo apt-get install python3-pip

Then run:

    pip3 install praw
    pip3 install prawcore
    pip3 install requests

### Reddit App Setup
1. Login to the account you want to delete comments/posts for
2. Go [here](https://www.reddit.com/prefs/apps/) and click the "are you a developer? create an app..." button.
3. Give it a name and select script as the type.
4. Put the redirect uri as http://127.0.0.1:65010/authorize_callback
5. Click create app and take note of the client ID and client secret. 

Here is an example of getting the client ID and client secret from a Reddit app:
![Example Reddit App](https://image.prntscr.com/image/VuV-R5LnQ36YWdHVloDAaw.png)

### App Setup
Open ``commentdeleter.py`` and add your Reddit username, password, client ID, and client secret to the fields ``USERNAME``, ``PASSWORD``, ``CLIENT_ID``, ``CLIENT_SECRET`` in the file. Add the subreddit name (without r/) you want to delete posts from to the ``SUBREDDIT`` field.

Read [this](https://www.reddit.com/r/RequestABot/comments/cyll80/a_comprehensive_guide_to_running_your_reddit_bot/) if you have issues with the overall setup/installation process.


## Usage

After you have added your Reddit information to ``commentdeleter.py`` and saved it, navigate to the file directory in the terminal or command prompt,  and run:
``python commentdeleter.py``

If typing ``python`` gives you Python 2, type this to run the script with Python 3:
``python3 commentdeleter.py``

The script will gather all your comments and posts from the subreddit and delete them. This will take a while (400 comments and 20 posts took around 20 minutes) so please be patient.