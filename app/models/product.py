import json
import requests
import os
from bs4 import BeautifulSoup
from app.utils import get_item
from app.models.opinion import Opinion
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt, rc_params_from_file

class Product():
    def __init__(self, product_id, product_name="", opinions=[], opinions_count=0, pros_count=0, cons_count=0, average_score=0):
        self.product_name=product_name
        self.product_id=product_id
        self.opinions=opinions
        self.opinions_count=opinions_count
        self.pros_count=pros_count
        self.cons_count=cons_count
        self.average_score=average_score
        return self

    def extract_name(self):
        url = f"https://www.ceneo.pl/{self.product_id}#tab=reviews"
        response = requests.get(url)
        page = BeautifulSoup(response.text, "html.parser")
        self.product_name = get_item(page, "h1.product-top__product-info__name")

        return self
    
    def extract_opinions(self):
        url = f"https://www.ceneo.pl/{self.product_id}#tab=reviews"
        all_opinions = []
        while(url):
            response = requests.get(url)
            page = BeautifulSoup(response.text, "html.parser")
            opinions = page.select("div.js_product-review")
            for opinion in opinions:
                single_opinion = Opinion().extract_opinion(opinion)
                self.opinions.append(single_opinion)
            try:
                url = "https://www.ceneo.pl"+get_item(page, "a.pagination__next", "href")
            except TypeError:
                url = None
        return self

    def opinions_to_df(self):
        return pd.read_json(json.dumps([opinion.to_dict() for opinion in self.opinions]))

    def calculate_stats(self):

        self.opinions_to_df()
        opinions["stars"] = opinions["stars"].map(lambda x: float(x.split("/")[0].replace(",", ".")))

        self.opinions_count = len(opinions)
        self.pros_count = opinions["pros"].map(bool).sum()
        self.cons_count = opinions["cons"].map(bool).sum()
        self.average_score = opinions["stars"].mean().round(2)

        return self

    def draw_charts(self):
        self.opinions_to_df()

        if not os.path.exists("app/plots"):
            os.mkdir("app/plots")

        recommendation = opinions["recommendation"].value_counts(dropna=False).sort_index().reindex(["Nie polecam", "Polecam", None], fill_value=0)
        recommendation.plot.pie(
            label="",
            autopct= lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '',
            colors = ["crimson","forestgreen","lightgrey"],
            labels=["Nie polecam","Polecam","Nie mam zdania"]

        )
        plt.title("Rekomendacje")
        plt.savefig(f"app/static/plots/{self.product_id}_recommendations.png")
        plt.close()

        stars = opinions["stars"].value_counts().sort_index().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
        stars.plot.bar(
            color = "#fbec5d"
        )

        plt.title("Oceny produktów")
        plt.xlabel("Liczba gwiazdek")
        plt.ylabel("Liczba opinii")
        plt.grid(True, axis="y")
        plt.xticks(rotation=0)
        plt.savefig(f"app/static/plots/{self.product_id}_stars.png")
        plt.close()

        return self
    
    def __str__(self):
        return f"""product_id: {self.product_id}<br>
        product_name: {self.product_name}<br>
        opinions_count: {self.opinions_count}<br>
        pros_count: {self.pros_count}<br>
        cons_count: {self.cons_count}<br>
        average_score: {self.average_score}<br>
        opinions: <br><br>
        """ + "<br><br>".join(str(opinion) for opinion in self.opinions)

    def __repr__(self):
        return f"Product(product_id={self.product_id}, product_name={self.product_name}, opinions_count={self.opinions_count}, pros_count={self.pros_count}, cons_count={self.cons_count}, average_score={self.average_score}, opinions: [" + ", ".join(opinion.__repr__() for opinion in self.opinions) + "])"

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "opinions_count": self.opinions_count,
            "pros_count": self.pros_count,
            "cons_count": self.cons_count,
            "average_score": self.average_score,
            "opinions": [opinion.to_dict() for opinion in self.opinions]
        }      

    def export_opinions(self):
        if not os.path.exists("app/opinions"):
            os.mkdir("app/opinions")
        
        with open(f"app/opinions/{self.product_id}.json", "w", encoding="UTF-8") as jf:
            json.dump([opinion.to_dict() for opinion in self.opinions], jf, indent=4, ensure_ascii=False)
            
        pass

    def export_product(self):
        pass