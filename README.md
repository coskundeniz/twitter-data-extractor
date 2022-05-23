Twitter Data Extractor
======================


## User data to extract

* Default
    * id
    * name
    * username

* Additional
    * created_at
    * description (bio)
    * entities (hashtags, urls, user mentions)
    * location
    * pinned_tweet_id
    * profile_image_url
    * protected
    * public_metrics (followers, friends, tweets, listed counts)
    * url
    * verified
    * pinned_tweet_text if pinned_tweet_id exists

-------------

## Columns for file reporters

```
[
    "ID",
    "Username",
    "Name",
    "Created At",
    "Bio",
    "URLs",
    "Hashtags",
    "Mentions",
    "Location",
    "Pinned Tweet ID",
    "Pinned Tweet",
    "Profile Image URL",
    "Account Protected",
    "Public Metrics",
    "Url",
    "Verified",
]
```