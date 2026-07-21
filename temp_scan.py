import re
from pathlib import Path
from html.parser import HTMLParser

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack=[]
        self.skip=False
        self.results=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag in {'script','style'}:
            self.skip=True
        self.stack.append((tag,attrs))
    def handle_endtag(self, tag):
        if tag in {'script','style'}:
            self.skip=False
        if self.stack:
            self.stack.pop()
    def handle_data(self, data):
        if self.skip: return
        data=data.strip()
        if not data: return
        # find nearest parent tag
        for i in range(len(self.stack)-1,-1,-1):
            tag,attrs=self.stack[i]
            if tag in {'script','style'}:
                return
            if tag in {'html','body','main','div','section','nav','footer','button','a','span','p','h1','h2','h3','li','ul','svg','path','line','polyline','rect','circle','img','strong','em','blockquote','option'}:
                if 'data-en' not in attrs and not attrs.get('aria-label') and tag not in {'img'}:
                    if data not in {'?','8','•'} and not data.startswith('http') and not data.startswith('file://'):
                        self.results.append((tag, data))
                break

text=Path('index.html').read_text(encoding='utf-8')
p=Parser(); p.feed(text)
for tag, data in p.results:
    print(f'{tag}: {data}')
