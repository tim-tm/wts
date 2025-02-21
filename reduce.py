from lxml import etree
import json
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from common import Page, Base

engine = create_engine("sqlite:///data.db")
Base.metadata.create_all(engine)
session = Session(engine)

class PageData:
    def __init__(self, page, root):
        page_title = page.find("title", namespaces=root.nsmap)
        if page_title is not None:
            self.title = page_title.text
        else:
            self.title = None

        page_id = page.find("id", namespaces=root.nsmap)
        if page_id is not None:
            self.id = page_id.text
        else:
            self.id = None

        rev = page.find("revision", namespaces=root.nsmap)
        if rev is not None:
            rev_text = rev.find("text", namespaces=root.nsmap)
            self.text = rev_text.text
            #self.text = re.sub("\\[\\[[^\\[]*\\]\\]", "", self.text) 
            self.text = re.sub("<.*\\/>", "", self.text) 
            self.text = re.sub("<.*>.*<\\/.*>", "", self.text) 
            self.text = re.sub("<!--.*-->", "", self.text) 
            self.text = re.sub("{{[^}]*}}", "", self.text)
            self.text = re.sub("\\[\\[", "", self.text)
            self.text = re.sub("\\]\\]", "", self.text)
            self.text = re.sub("'''", "", self.text)
            self.text = re.sub("''", "", self.text)
            self.text = re.sub("==[^=]*==", "", self.text)
            self.text = re.sub("\\n", "", self.text)

        # timestamp = rev.find("timestamp", namespaces=root.nsmap)
        # self.time = datetime.strptime(timestamp.text, "%Y-%m-%dT%H:%M:%SZ")
        # contributor = rev.find("contributor", namespaces=root.nsmap)
        # contributor_name = contributor.find("username", namespaces=root.nsmap)
        # if contributor_name is not None:
        #     self.username = contributor_name.text
        # else:
        #     self.username = None

    def __str__(self):
        return self.title

    def toDict(self):
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text
        } 


tree = etree.parse("dewiki-multistream5.xml")
root = tree.getroot()

for i, page in enumerate(root.findall("page", namespaces=root.nsmap)):
    if i > 10:
        break

    p = PageData(page, root)
    pg = Page(title=p.title, text=p.text)
    session.add(pg)
    session.commit()
