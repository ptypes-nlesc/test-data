import pandas as pd


class TagReducer:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    def reduce_to_popular_tags(self):
        # Extract tags from categories
        self.df["tags"] = self.df.categories.apply(
            lambda x: x.replace("['", "").replace("']", "").replace("'", "").split(", ")
        )

        # Flatten tags
        df_flat_tag = pd.DataFrame(
            [tag for tag_list in self.df.tags for tag in tag_list], columns=["tag"]
        )

        # Count tag appearances
        popular_tags = (
            df_flat_tag.groupby("tag")
            .size()
            .reset_index(name="counts")
            .sort_values("counts", ascending=False)
            .reset_index(drop=True)
        )

        # Calculate the 3rd quantile to find popular tags
        counts = df_flat_tag.groupby(["tag"]).size().reset_index(name="counts").counts
        min_appearance = counts.quantile(0.70)

        # Find popular tags - make into Python set for efficiency
        popular_tags_set = set(
            popular_tags[popular_tags.counts >= min_appearance]["tag"]
        )

        # Reduce tags to popular tags
        self.df["popular_tags"] = self.df.tags.apply(
            lambda tag_list: [tag for tag in tag_list if tag in popular_tags_set]
        )

        # Filter rows with no popular tags
        self.df = self.df.loc[
            self.df.popular_tags.apply(lambda tag_list: tag_list != [])
        ]


# if __name__ == "__main__":
#     tag_reducer = TagReducer("porn-with-dates-2022.csv")
#     tag_reducer.reduce_to_popular_tags()
#     df = tag_reducer.df
