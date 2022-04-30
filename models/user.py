from dataclasses import dataclass, field


@dataclass
class User:

    user: tuple
    data: dict = field(default_factory=dict, init=False)

    def __post_init__(self):
        self._fields, self._includes = self.user

        self.data["id"] = self._fields.id
        self.data["name"] = self._fields.name
        self.data["username"] = self._fields.username

    def __str__(self) -> str:

        user_data_format = f"{self._fields.id}:{self._fields.username}:{self._fields.name}\n"

        user_data_format += f"\tCreated at: {self._fields.created_at}\n"
        user_data_format += f"\tBio: {self._fields.description}\n"

        if self._fields.entities:
            entities = self._fields.entities

            if "url" in entities:
                user_data_format += "\tURLs\n"
                for url_item in entities["url"]["urls"]:
                    user_data_format += f"\t\t{url_item['url']}\n"

            if "description" in entities:
                if "hashtags" in entities["description"]:
                    user_data_format += "\tHashtags\n"
                    for hashtag_item in entities["description"]["hashtags"]:
                        user_data_format += f"\t\t{hashtag_item['tag']}\n"

                if "mentions" in entities["description"]:
                    user_data_format += "\tMentions\n"
                    for mention_item in entities["description"]["mentions"]:
                        user_data_format += f"\t\t{mention_item['username']}\n"

        user_data_format += f"\tLocation: {self._fields.location}\n"

        user_data_format += f"\tPinned tweet id: {self._fields.pinned_tweet_id}\n"
        if self._includes:
            user_data_format += f"\tPinned tweet: {self._includes['tweets'][0]['text']}\n"

        user_data_format += f"\tUser profile image url: {self._fields.profile_image_url}\n"
        user_data_format += f"\tIs account private: {'YES' if self._fields.protected else 'NO'}\n"

        user_data_format += "\tPublic metrics\n"
        for metric, value in self._fields.public_metrics.items():
            user_data_format += f"\t\t{metric}: {value}\n"

        user_data_format += f"\tUrl: {self._fields.url}\n"
        user_data_format += f"\tVerified: {self._fields.verified}\n"

        return user_data_format
