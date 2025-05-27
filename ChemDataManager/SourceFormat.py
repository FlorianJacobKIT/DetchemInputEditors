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
        self.author = ""
        self.title = ""
        self.creation_date = datetime.date.today()
        self.publisher = ""
        self.source_type = ""
        self.link = ""
        self.comment = ""