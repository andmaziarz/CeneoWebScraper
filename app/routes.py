from math import prod
from app import app
from flask import redirect, render_template
from cmath import sin
from typing import Type
from urllib import response
import requests
import json
from turtle import st
from bs4 import BeautifulSoup

@app.route('/')

def index():
    return render_template('index.html.jinja')

@app.route('/extract/<product_id>')
def extract(product_id):
    def get_item(ancestor, selector, attribute=None, return_list=False):
        try:
            if return_list:
                return [item.get_text().strip() for item in ancestor.select(selector)]
            if attribute:
                return ancestor.select_one(selector)[attribute]
            return ancestor.select_one(selector).get_text().strip()
        except (AttributeError, TypeError):
            return None

    selectors = {
        "author": ["span.user-post__author-name"],
        "recommendation": ["span.user-post__author-recomendation > em"],
        "stars": ["span.user-post__score-count"],
        "content": ["div.user-post__text"],
        "useful": ["button.vote-yes > span"],
        "useless": ["button.vote-no > span"],
        "published": ["span.user-post__published > time:nth-child(1)", "datetime"],
        "purchased": ["span.user-post__published > time:nth-child(2)", "datetime"],
        "pros": ["div[class$=positives] ~ div.review-feature__item", None, True],
        "cons": ["div[class$=negatives] ~ div.review-feature__item", None, True]
    }

    url ="https://www.ceneo.pl/{product_id}#tab=reviews"
    all_opinions = []

    while (url):
        response = requests.get(url)

        page = BeautifulSoup(response.text, "html.parser")
            
        opinions = page.select("div.js_product-review")
        for opinion in opinions:
            opinion_id = opinion["data-entry-id"]
            author = opinion.select_one("span.user-post__author-name").get_text().strip()
            try:
                recommendation = opinion.select_one("span.user-post__author-recomendation > em").get_text().strip()
            except AttributeError:
                recommendation = None
                stars = opinion.select_one("span.user-post__score-count").get_text().strip()
                content = opinion.select_one("div.user-post__text").get_text().strip()
                useful = opinion.select_one("button.vote-yes > span").get_text().strip()
                useless = opinion.select_one("button.vote-no > span").get_text().strip()
                published = opinion.select_one("span.user-post__published > time:nth-child(1)")["datetime"]
            try:
                purchased = opinion.select_one("span.user-post__published > time:nth-child(2)")["datetime"]
            except TypeError:
                purchased = None
                pros = opinion.select("div[class$=positives] ~ div.review-feature__item")
                pros = [item.get_text().strip() for item in pros]
                cons = opinion.select("div[class$=negatives] ~ div.review-feature__item")
                cons = [item.get_text().strip() for item in cons]

            single_opinion = {
                "opinion_id" : opinion_id,
                "author" : author,
                "recommendation" : recommendation,
                "stars" : stars,
                "content" : content,
                "useful" : useful,
                "useless" : useless,
                "published" : published,
                "purchased" : purchased,
                "pros" : pros,
                "cons" : cons
            }

            all_opinions.append(single_opinion)
            try:
                url = "https://www.ceneo.pl"+page.select_one("a.pagination__next")["href"]
            except TypeError:
                url = None

        with open(f"app/opinions/{product_id}.json", "w", encoding="utf-8") as jf:
            json.dump(all_opinions, jf, indent = 4, ensure_ascii=False)

        return redirect(url_for('product', product_id=product_id))
            

@app.route('/products')
def products(product_id):
    return render_template('products.html.jinja')

@app.route('/author')
def author():
    return render_template('author.html.jinja')

@app.route('/product/<product_id>')
def product(product_id):
    return render_template('product.html.jinja', product_id=product_id)