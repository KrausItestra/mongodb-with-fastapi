from enum import Enum

class BeverageCategory(str, Enum):
    coffee = "coffee"
    tea = "tea"
    soda = "soda"
    water = "water"
    juice = "juice"
    energy = "energy"
    alcohol = "alcohol"
    other = "other"

class SnackCategory(str, Enum):
    cookies = "cookies"
    candy = "candy"
    chips = "chips"
    nuts = "nuts"
    fruit = "fruit"
    chocolate = "chocolate"
    other = "other"
