import pandas as pd


class TagReducer:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    @staticmethod
    def extract_tags(categories):
        return (
            categories.replace("['", "").replace("']", "").replace("'", "").split(", ")
        )

    @staticmethod
    def flatten_tags(tags):
        return pd.DataFrame(
            [tag for tag_list in tags for tag in tag_list], columns=["tag"]
        )

    @staticmethod
    def get_popular_tags(df_flat_tag, quantile=0.90):
        popular_tags = (
            df_flat_tag.groupby("tag")
            .size()
            .reset_index(name="counts")
            .sort_values("counts", ascending=False)
            .reset_index(drop=True)
        )
        min_appearance = popular_tags.counts.quantile(quantile)
        return set(popular_tags[popular_tags.counts >= min_appearance]["tag"])

    @staticmethod
    def filter_popular_tags(tag_list, popular_tags_set):
        return [tag for tag in tag_list if tag in popular_tags_set]

    def reduce_to_popular_tags(self, quantile=0.90):
        """
        Reduce the tags to only include popular tags.

        Parameters:
        - quantile (float): The quantile value used to determine
        the minimum appearance count for a tag to be considered popular.
        Default is 0.90.

        Returns:
        None
        """

        # Extract tags from categories
        self.df["tags"] = self.df.categories.apply(self.extract_tags)

        # Flatten tags
        df_flat_tag = self.flatten_tags(self.df.tags)

        # Get popular tags
        popular_tags_set = self.get_popular_tags(df_flat_tag, quantile)

        # Reduce tags to popular tags
        self.df["popular_tags"] = self.df.tags.apply(
            lambda tag_list: self.filter_popular_tags(tag_list, popular_tags_set)
        )

        # Filter rows with no popular tags
        self.df = self.df.loc[
            self.df.popular_tags.apply(lambda tag_list: tag_list != [])
        ]


if __name__ == "__main__":
    # Create an instance of TagReducer
    reducer = TagReducer("porn-with-dates-2022.csv")

    # Reduce tags to popular tags
    reducer.reduce_to_popular_tags(quantile=0.99)

    # Print the DataFrame with popular tags
    print(reducer.df)
