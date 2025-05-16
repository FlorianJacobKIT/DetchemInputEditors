import datetime


class Source():
    ID: int
    author: str
    title: str
    creation_date: datetime.date
    publisher: str
    source_type: str
    link: str
    comment: str

    def __init__(self, ID):
        self.ID = ID