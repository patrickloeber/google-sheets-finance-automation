import csv, requests
from enum import Enum

class CATEGORY(Enum):
    FEES = "Fees"
    EATING_OUT = "Eating Out"
    SELF_DEVELOPMENT = "Self Development"
    FOOD = "Food"
    HEALTH = "Health"
    PHONE = "Phone/Internet"
    CAR = "Car"
    CLOTHES = "Clothes"
    MISC = "Misc."
    SHOPPING = "Shopping"
    HOUSING = "Housing"
    ENTERTAINMENT = "Entertainment"


class IMPORTANCE(Enum):
    SHOULDNT_HAVE = "Shouldn't Have"
    NICE_TO_HAVE = "Nice to Have"
    HAVE_TO_HAVE = "Have to Have"
    ESSENTIAL = "Essential"


class Expense:
    def __init__(self, item, price):
        self.item = item
        self.price = price
        self.category, self.importance = self._determine_category_and_importance()

    def _determine_category_and_importance(self):
        item = self.item.lower()
        if item in ["fee"]:
            return CATEGORY.FEES, IMPORTANCE.SHOULDNT_HAVE
        if item in ["uber eats", "pizza"]:
            return CATEGORY.EATING_OUT, IMPORTANCE.NICE_TO_HAVE
        if item in ["book"]:
            return CATEGORY.SELF_DEVELOPMENT, IMPORTANCE.NICE_TO_HAVE
        if item in ["groceries"]:
            return CATEGORY.FOOD, IMPORTANCE.ESSENTIAL
        if item in ["gym"]:
            return CATEGORY.HEALTH, IMPORTANCE.HAVE_TO_HAVE
        if item in ["phone"]:
            return CATEGORY.PHONE, IMPORTANCE.ESSENTIAL
        if item in ["gas", "car"]:
            return CATEGORY.CAR, IMPORTANCE.HAVE_TO_HAVE
        if item in ["clothes"]:
            return CATEGORY.CLOTHES, IMPORTANCE.NICE_TO_HAVE
        if item in ["movies"]:
            return CATEGORY.ENTERTAINMENT, IMPORTANCE.NICE_TO_HAVE
        if item in ["ikea"]:
            return CATEGORY.SHOPPING, IMPORTANCE.NICE_TO_HAVE
        if item in ["rent"]:
            return CATEGORY.HOUSING, IMPORTANCE.ESSENTIAL
        return CATEGORY.MISC, IMPORTANCE.NICE_TO_HAVE


    def __repr__(self) -> str:
        return f"{self.item},{self.category.value},{self.price},{self.importance.value}"

def get_data():
    expenses_url = "https://PLACE_GOOGLE_SHEETS_URL_HERE"
    # Sample url: "https://docs.google.com/spreadsheets/d/e/2PACX-1vTw71oo5J_2Ov8eqgMczD3u6lMuHj_YYYCvOKCH9WGa6KdNjH-sHn062KOc-aH73npIGAqKQIewqfQg/pub?output=csv"
    expenses_csv = requests.get(expenses_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=(3, 5))
    reader = csv.reader(expenses_csv.text.splitlines())

    expenses = []
    for row in reader:
       expenses.append(Expense(row[0], row[1]))

    return expenses