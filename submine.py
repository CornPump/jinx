import os
import credentials
import praw
import helpers
import time

REDDIT_THREAD_LIMIT = 1000
REDDIT_API_TRIES = 3

class Submine:

    def __init__(self,sub_name,post_name,limit=None,origin_dir=False):
        # Reddit instance, created from reddit credentials
        self.reddit = praw.Reddit(client_id=credentials.REDDIT_OAUTH_ID,
                            client_secret=credentials.REDDIT_OAUTH_PW,
                             user_agent='Comment read automation',
                             )
        # Reddit sub name
        self.sub_name = sub_name
        # reddit post_name to mine comments from, will mine posts that contains this string
        self.post_name = post_name
        # number of maximum posts of such name to mine
        if limit != None:
            if limit <= 1:
                self.limit = 1
            elif limit > REDDIT_THREAD_LIMIT:
                self.limit = None
            else:
                self.limit = limit
        else:
            self.limit = limit
        # Directory underneath to place the output files in
        if not origin_dir or not os.path.exists(origin_dir):
            self.origin_dir = os.getcwd()
        else:
            self.origin_dir = origin_dir

    def __str__(self):
        return f"{{'sub_name':{self.sub_name},'post_name':{self.post_name}," \
               f"'limit':{self.limit}, 'working_dir':{self.origin_dir}}}"

    def params(self):
        return {'sub_name': self.sub_name, 'post_name': self.post_name,
         'limit': self.limit, 'working_dir': self.origin_dir}

    # check if reddit credentials are valid
    def validate_reddit_credentials(self):
        try:
            subreddit = self.reddit.subreddit(self.sub_name)
            for thread_id in subreddit.new(limit=1):
                submission = self.reddit.submission(thread_id)
            return True
        except:
            return False

    # this function scraps the whole sub
    # if is_whole param =False, files that already exists in directory won't be scraped again
    def scrap_whole_sub(self,is_whole=True):
        # prepare sub and working dir
        subreddit = self.reddit.subreddit(self.sub_name)
        working_dir = helpers.files.create_directory(self.sub_name,self.origin_dir)
        # go over each thread in the sub
        thread_limit = self.limit
        for thread_id in subreddit.new(limit=None):
            if thread_limit != None:
                if not thread_limit:
                    break
            submission = self.reddit.submission(thread_id)
            # check if current thread is of the same series, if not skip it
            if not self.post_name.lower() in submission.title.lower():
                continue
            if thread_limit != None:
                thread_limit -= 1
            # create file name
            creation_date_utc = submission.created_utc
            file_name = helpers.files.create_file_name(self.post_name,working_dir,creation_date_utc)

            # for partial filling of missing files, if file exists continue running
            if not is_whole and os.path.exists(file_name):
                print('File already exist, skipping: ',os.path.basename(file_name))
                continue

            # api calls for receiving all post's comments (very heavy & Reddit time limits)
            succeed = REDDIT_API_TRIES
            while succeed > 0:
                try:
                    print(f'Loading all comments through Reddit api for {os.path.basename(file_name)} ..')
                    submission.comments.replace_more(limit=None)
                    succeed = -1
                except Exception as error:
                    print(f"Error of rate limit occurred: \n{error}")
                    succeed -= 1
                    if not succeed:
                        print(f"Failed {REDDIT_API_TRIES} times, leaving out file {os.path.basename(file_name)}")
                    print("Trying again in 50 seconds...")
                    time.sleep(50)
            # If after 3 tries current comments threads won't load, cut the file out.
            if not succeed:
                continue
            # save all comments and dump them into a json file
            comments = []
            for comment in submission.comments.list()[1:]:
                if comment == "[deleted]":
                    continue
                comments.append({'body': comment.body})

            helpers.files.save_comments_to_file(file_name,comments)








