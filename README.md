Twitter Data Extractor
======================

This command-line tool extracts user and tweet data from Twitter and reports the results to CSV, Excel, Google Sheets documents or MongoDB, SQLite databases.

### Supported Features

* Extract single/multiple user data.
* Extract user’s friends/followers data.
* Extract tweets data for a user.
* Extract tweets data for a search keyword.
* Report results to CSV, Excel or Google Sheets documents.
* Report results to MongoDB or SQLite databases.


## How to setup

* Run the following commands to install required packages in the project directory.

    * `python -m venv env`
    * `source env/bin/activate`
    * `python -m pip install -r requirements.txt`


### Setting Environment Variables

If you will use your own Twitter API credentials, set the *TWITTER_BEARER_TOKEN_CODE* environment variable with your bearer token value.

If you will use my account on behalf of your account, send email to support email at the end of this document to get my consumer key and secret tokens and set these to *TWITTER_CONSUMER_KEY_CODE* and *TWITTER_CONSUMER_SECRET_CODE* environment variables.


### MongoDB Installation

If you will use MongoDB to save users/tweets data, install it from [here](https://docs.mongodb.com/manual/administration/install-community/).

You can check the running status after installation and start the database server with the following commands on Linux.

* `sudo service mongod status`
* `sudo service mongod start`


## How to use

```sh
usage: python twitter_data_extractor.py [-h] [-c] [-cf CONFIGFILE] [--forme] [-u USER] [-ul USERS] [-fr] [-fl] [-ut] [-s SEARCH]
                                        [-tc TWEET_COUNT] [-e EXCLUDES] [-ot OUTPUT_TYPE] [-of OUTPUT_FILE] [-sm SHARE_MAIL]

optional arguments:
  -h, --help                                  show this help message and exit
  -c, --useconfig                             Read configuration from config.json file
  -cf CONFIGFILE, --configfile CONFIGFILE     Read configuration from given file
  --forme                                     Determine API user(account owner or on behalf of a user)
  -u USER, --user USER                        Extract user data for the given username
  -ul USERS, --users USERS                    Extract user data for the given comma separated usernames
  -fr, --friends                              Extract friends data for the given username
  -fl, --followers                            Extract followers data for the given username
  -ut, --user_tweets                          Extract tweets of user with the given username
  -s SEARCH, --search SEARCH                  Extract latest tweets for the given search keyword
  -tc TWEET_COUNT, --tweet_count TWEET_COUNT  Limit the number of tweets gathered
  -e EXCLUDES, --excludes EXCLUDES            Fields to exclude from tweets queried as comma separated values (replies,retweets)
  -ot OUTPUT_TYPE, --output_type OUTPUT_TYPE  Output file type (csv, xlsx, gsheets, mongodb or sqlite)
  -of OUTPUT_FILE, --output_file OUTPUT_FILE  Output file name
  -sm SHARE_MAIL, --share_mail SHARE_MAIL     Mail address to share Google Sheets document
```

* If config will be used for getting parameters, boolean parameters like --forme, --friends still must be passed as command-line option.
* "user" and "users" field should be empty for "search" keyword to be used.


### Basic Usage

The following commands are a few examples of getting user data, user’s friends, tweets or tweets of a given keyword.

* `python twitter_data_extractor.py -u gvanrossum`
* `python twitter_data_extractor.py --forme -ul "gvanrossum,nedbat"`
* `python twitter_data_extractor.py -u gvanrossum -fr`
* `python twitter_data_extractor.py --forme -u gvanrossum -ut`
* `python twitter_data_extractor.py -s python`

Results are written to *results.xlsx* file by default.
Logs can be seen in the *tw_data_extractor.log* file in the project directory.


### Example Commands

* Get user data for username gvanrossum and save results to results.xlsx file.
    * `python twitter_data_extractor.py -u gvanrossum`

* Get user data for username gvanrossum and save results to results.xlsx file with your own Twitter API credentials.
    * `python twitter_data_extractor.py --forme -u gvanrossum`

* Get user data for usernames gvanrossum and nedbat.
    * `python twitter_data_extractor.py -ul "gvanrossum,nedbat"`

* Get friends data for username gvanrossum and save results to results.csv file.
    * `python twitter_data_extractor.py -u gvanrossum -fr -ot csv -of results.csv`

* Get followers data for username gvanrossum.
    * `python twitter_data_extractor.py -u gvanrossum -fl`

* Get the last tweets data for username gvanrossum.
    * `python twitter_data_extractor.py --forme -u gvanrossum -ut`

* Get the last 50 tweets data for username gvanrossum and exclude both replies and retweets.
    * `python twitter_data_extractor.py --forme -u gvanrossum -ut -tc 50 -e "replies,retweets"`

* Get the last 50 tweets data for keyword python.
    * `python twitter_data_extractor.py -s python -tc 50`

* Get the last tweets data for keyword python and write results to Google Sheets document with name last_tweets and share with the given email.
    * `python twitter_data_extractor.py -s python -ot gsheets -of last_tweets -sm codenineeight@gmail.com`

---

## Support

If you need support, you can contact me by emailing to codenineeight@gmail.com with the “twitter_data_extractor” prefix in the subject. You can also see my Upwork profile [here](https://www.upwork.com/freelancers/~011e3fe44e575092f0).
