from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class User:

    user: tuple
    data: dict = field(default_factory=dict, init=False)

    def __post_init__(self):
        """Construct the data dictionary for the User model for reporters"""

        self._fields, self._includes = self.user

        self.data["id"] = self._fields.id
        self.data["name"] = self._fields.name
        self.data["username"] = self._fields.username

        self.data["created_at"] = self._fields.created_at
        self.data["description"] = self._fields.description

        self.data["entities"] = defaultdict(dict)

        if self._fields.entities:
            entities = self._fields.entities

            if "url" in entities:
                self.data["entities"]["url_items"] = []

                for url_item in entities["url"]["urls"]:
                    self.data["entities"]["url_items"].append(url_item["url"])

            if "description" in entities:
                self.data["entities"]["hashtag_items"] = []

                if "hashtags" in entities["description"]:
                    for hashtag_item in entities["description"]["hashtags"]:
                        self.data["entities"]["hashtag_items"].append(hashtag_item["tag"])

                if "mentions" in entities["description"]:
                    self.data["entities"]["mention_items"] = []
                    for mention_item in entities["description"]["mentions"]:
                        self.data["entities"]["mention_items"].append(mention_item["username"])

        self.data["location"] = self._fields.location

        self.data["pinned_tweet_id"] = str(self._fields.pinned_tweet_id)

        if self._includes:
            try:
                self.data["pinned_tweet_text"] = self._includes["tweets"][0]["text"]
            except KeyError:
                # get pinned tweet text for get_friends/followers includes field
                self.data["pinned_tweet_text"] = self._includes["text"]
        else:
            self.data["pinned_tweet_text"] = ""

        self.data["profile_image_url"] = self._fields.profile_image_url
        self.data["protected"] = self._fields.protected

        self.data["public_metrics"] = self._fields.public_metrics

        self.data["url"] = self._fields.url
        self.data["verified"] = self._fields.verified

    def __str__(self) -> str:

        user_data_format = f"{self.data['id']}:{self.data['username']}:{self.data['name']}\n"

        user_data_format += f"\tCreated at: {self.data['created_at']}\n"
        user_data_format += f"\tBio: {self.data['description']}\n"

        if self._fields.entities:

            user_data_format += "\tURLs\n" if self.data["entities"]["url_items"] else ""
            for url_item in self.data["entities"]["url_items"]:
                user_data_format += f"\t\t{url_item}\n"

            user_data_format += "\tHashtags\n" if self.data["entities"]["hashtag_items"] else ""
            for hashtag_item in self.data["entities"]["hashtag_items"]:
                user_data_format += f"\t\t{hashtag_item}\n"

            user_data_format += "\tMentions\n" if self.data["entities"]["mention_items"] else ""
            for mention_item in self.data["entities"]["mention_items"]:
                user_data_format += f"\t\t{mention_item}\n"

        user_data_format += f"\tLocation: {self.data['location']}\n"

        user_data_format += f"\tPinned tweet id: {self.data['pinned_tweet_id']}\n"
        if self._includes:
            user_data_format += f"\tPinned tweet: {self.data['pinned_tweet_text']}\n"

        user_data_format += f"\tProfile image url: {self.data['profile_image_url']}\n"
        user_data_format += f"\tIs account private: {'YES' if self.data['protected'] else 'NO'}\n"

        user_data_format += "\tPublic metrics\n"
        for metric, value in self.data["public_metrics"].items():
            user_data_format += f"\t\t{metric}: {value}\n"

        user_data_format += f"\tUrl: {self.data['url']}\n"
        user_data_format += f"\tVerified: {self.data['verified']}\n"

        return user_data_format
