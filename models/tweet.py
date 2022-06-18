from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class Tweet:

    tweet: tuple
    data: dict = field(default_factory=dict, init=False)

    def __post_init__(self):
        """Construct the data dictionary for the Tweet model for reporters"""

        self._fields, self._includes = self.tweet

        self.data["id"] = self._fields.id
        self.data["text"] = self._fields.text
        self.data["created_at"] = self._fields.created_at
        self.data["source"] = self._fields.source
        self.data["language"] = self._fields.lang
        self.data["public_metrics"] = self._fields.public_metrics

        self.data["entities"] = defaultdict(dict)

        if self._fields.entities:
            entities = self._fields.entities

            if "urls" in entities:
                self.data["entities"]["url_items"] = []
                for url_item in entities["urls"]:
                    self.data["entities"]["url_items"].append(url_item["url"])

            if "hashtags" in entities:
                self.data["entities"]["hashtag_items"] = []
                for hashtag_item in entities["hashtags"]:
                    self.data["entities"]["hashtag_items"].append(hashtag_item["tag"])

            if "mentions" in entities:
                self.data["entities"]["mention_items"] = []
                for mention_item in entities["mentions"]:
                    self.data["entities"]["mention_items"].append(mention_item["username"])

        self.data["media"] = []
        self.data["places"] = []

        if self._includes:

            if "media" in self._includes:
                for media_item in self._includes["media"]:
                    self.data["media"].append(media_item)

            if "places" in self._includes:
                for place_item in self._includes["places"]:
                    self.data["places"].append(place_item)

    def __str__(self) -> str:

        tweet_data_format = f"ID: {self.data['id']}\n"
        tweet_data_format += f"\tTweet: {self.data['text']}\n"
        tweet_data_format += f"\tCreated at: {self.data['created_at']}\n"
        tweet_data_format += f"\tSource: {self.data['source']}\n"
        tweet_data_format += f"\tLanguage: {self.data['language']}\n"

        tweet_data_format += "\tPublic Metrics\n"
        for metric, value in self.data["public_metrics"].items():
            tweet_data_format += f"\t\t{metric}: {value}\n"

        if self._fields.entities:

            tweet_data_format += "\tURLs\n" if self.data["entities"]["url_items"] else ""
            for url_item in self.data["entities"]["url_items"]:
                tweet_data_format += f"\t\t{url_item}\n"

            tweet_data_format += "\tHashtags\n" if self.data["entities"]["hashtag_items"] else ""
            for hashtag_item in self.data["entities"]["hashtag_items"]:
                tweet_data_format += f"\t\t{hashtag_item}\n"

            tweet_data_format += "\tMentions\n" if self.data["entities"]["mention_items"] else ""
            for mention_item in self.data["entities"]["mention_items"]:
                tweet_data_format += f"\t\t{mention_item}\n"

        tweet_data_format += "\tMedia\n" if self.data.get("media") else ""
        for media in self.data["media"]:
            tweet_data_format += f"\t\tKey: {media['media_key']}, Type: {media['type']}\n"
            tweet_data_format += f"\t\tURL: {media['url']}\n"
            tweet_data_format += f"\t\tWidth: {media['width']}, Height: {media['width']}\n"

            if media["type"] == "video":
                tweet_data_format += f"\t\tDuration: {media['duration_ms']}\n"
                tweet_data_format += f"\t\tView count: {media['public_metrics']['view_count']}\n"

        tweet_data_format += "\tPlace\n" if self.data.get("place") else ""
        for place in self.data["places"]:
            tweet_data_format += f"\t\tID: {place['id']}\n\t\tFull name: {place['full_name']}\n"
            tweet_data_format += f"\t\tCountry: {place['country']} ({place['country_code']})\n"
            tweet_data_format += (
                f"\t\tType: {place['place_type']}, Coords: {place['geo']['bbox']}\n"
            )

        return tweet_data_format
