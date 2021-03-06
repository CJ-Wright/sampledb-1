#!/usr/bin/env python
import pandas as pd
from pprint import pformat
from functools import reduce


class SearchResult(object):
    """
    An object containing the matching results of a search on the database.
    """

    def __init__(self, results):
        """
        Create a SearchResult.
        """
        self.results = pd.DataFrame(results)
        if self.results.size == 0:
            return
        self.results.sort_values(list(self.results.columns), inplace=True)
        self.results.reset_index(drop=True, inplace=True)

    def __repr__(self):
        return pformat(self.results.T.to_dict())

    def __str__(self):
        return pformat(self.results.T.to_dict())

    def __eq__(self, other):
        if type(other) is type(self):
            return self.results.equals(other.results)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def filter(self, indices):
        """
        Filter the search results.
        Returns new SearchResult with only the filtered results.
        """
        df = self.results.filter(items=indices, axis=0)
        return SearchResult(df.reset_index(drop=True))

    def download(self, filename):
        """
        Download the search results as a spreadsheet.
        """
        frames = []
        for name in self.results:
            f = self.results[name].rename(name.replace('_', ' ').title())
            f = f.to_frame()
            frames.append(f)
        df = reduce(lambda x, y: x.join(y), frames)

        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        df.to_excel(writer, index=False)
        sheet = writer.sheets['Sheet1']
        for i, name in enumerate(df):
            width = max(len(str(val)) for val in df[name])
            width = max(width, len(name)) + 1
            sheet.set_column(i, i, width)
        writer.save()
