from flask import Markup
import markdown

con ="""
##Quict Start
###Adding Views

``` python
from flask import Flask
from flask.ext.admin import Admin, BaseView, expose
from .model import User, FavVideo, Article, db

class MyView(BaseView):
@expose('/')
 def index(self):
 return self.render('index.html')
```
"""
contents= Markup(markdown.markdown(con))
print(contents)
