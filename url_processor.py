import hashlib

import pandas as pd


class UrlProcessor:
    """
    A class used to process URLs in a DataFrame.

    ...

    Methods
    -------
    generate_id(url)
        Generates a unique identifier from a URL.
    add_id_column(df, url_column)
        Adds a new column with unique identifiers to a DataFrame.
    """

    @staticmethod
    def generate_id(url):
        """
        Generates a unique identifier from a URL.

        Parameters
        ----------
            url : str
                URL from which to generate the identifier

        Returns
        -------
            str
                a unique identifier generated from the URL
        """
        # Hash the URL using SHA-256 algorithm
        hashed_url = hashlib.md5(url.encode()).hexdigest()
        truncated_hash = hashed_url[:8]
        return truncated_hash

    @staticmethod
    def add_id_column(df, url_column):
        """
        Adds a new column with unique identifiers to a DataFrame.

        Parameters
        ----------
            df : pandas.DataFrame
                DataFrame to which to add the column
            url_column : str
                name of the column containing the URLs

        Returns
        -------
            None
        """
        df["id"] = df[url_column].apply(UrlProcessor.generate_id)


if __name__ == "__main__":
    # Create a sample DataFrame
    data = {
        "url": [
            "http://example.com/1",
            "http://example.com/2",
            "http://example.com/3",
        ]
    }
    dat = pd.DataFrame(data)

    # Create an instance of UrlProcessor
    processor = UrlProcessor()

    # Add a new column with unique identifiers to the DataFrame
    processor.add_id_column(dat, "url")

    # Print the DataFrame
    print(dat)
