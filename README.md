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

### Columns for file reporters

* User data columns

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

* Tweet data columns

```
[
    "ID",
    "Text",
    "Created At",
    "Source",
    "Language",
    "Public Metrics",
    "URLs",
    "Hashtags",
    "Mentions",
    "Media",
    "Place",
]
```

## User Tweet data to extract

* Default
    * id
    * text

* Additional
    * author_id (for search tweets)
    * attachments
    * created_at
    * entities (hashtags, urls, user mentions)
    * geo
    * lang
    * public_metrics (reply, retweet, like, quote counts)
    * source

* media_fields
    * url
    * duration_ms
    * width
    * height
    * public_metrics

* place_fields
    * country
    * country_code
    * geo
    * place_type

* expansions=geo.place_id,attachments.media_keys

* exclude="retweets"

