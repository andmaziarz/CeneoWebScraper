from app import parameters
from app.utils import get_item

class Opinion():
    def __init__(self, opinion_id="", author="", recommendation=None, stars=0, content="", pros=[], cons=[], useful=0, useless=0, published_date=None, purchased_date=None):
        self.opinion_id=opinion_id
        self.author=author
        self.recommendation=recommendation
        self.stars=stars
        self.content=content
        self.pros=pros
        self.cons=cons
        self.useful=useful
        self.useless=useless
        self.published_date=published_date
        self.purchased_date=purchased_date
        return self
    
    def extract_opinion(self, opinion):
        for key, value in selectors.items():
            setattr(self, key, get_item(opinion, *value))
            self.opinion_id = opinion["data-entry-id"]
        return self

    def __str__(self) -> str:
        return f"{self.author}, {self.recommendation}, {self.stars}, {self.content}, {self.useful}, {self.useless}, {self.publish_date}, {self.purchase_date}, {self.pros}, {self.cons}, {self.opinion_id}"
    
    def __repr__(self) -> str:
        return f"{self.author}, {self.recommendation}, {self.stars}, {self.content}, {self.useful}, {self.useless}, {self.publish_date}, {self.purchase_date}, {self.pros}, {self.cons}, {self.opinion_id}"

    def to_dict(self) -> dict:
        opinion_data ={
            "author" : self.author,
            "recommendation" : self.recommendation,
            "stars" : self.stars, 
            "content" : self.content,
            "useful" : self.useful,
            "useless" : self.useless,
            "publish_date" : self.publish_date,
            "purchase_date" : self.purchase_date,
            "pros" : self.pros,
            "cons" : self.cons,
            "opinion_id" : self.opinion_id
        }
        return opinion_data
        