import os
from crossWord import *
from drawing import *
import pickle
import sys
import requests
import re
from bs4 import BeautifulSoup
import random
from PIL import Image, ImageDraw ,ImageFont


c=CrossWord(15)
c.generate()
p,s=Draw(c)
p.save("problem.png")
s.save("solution.png")