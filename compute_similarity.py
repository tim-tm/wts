# import matplotlib.pyplot as plt
import spacy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from common import Page, Similarity

engine = create_engine("sqlite:///data.db")
session = Session(engine)
pages = session.query(Page).all()

nlp = spacy.load("de_core_news_md")
vecs = [nlp(page.text) for page in pages]
# similarity = []
for i, veci in enumerate(vecs):
    # row = []
    for j, vecj in enumerate(vecs):
        sim = Similarity(first=pages[i].id,
                         second=pages[j].id,
                         similarity=veci.similarity(vecj))
        session.add(sim)
        session.commit()
        # row.append(veci.similarity(vecj))
    # similarity.append(row)

# titles = [page.title for page in pages]

# plt.imshow(similarity)
# titles_range = range(len(titles))
# plt.xticks(titles_range, labels=titles,
#           rotation=45, ha="right",
#           rotation_mode="anchor")
# plt.yticks(titles_range, labels=titles)
# for i in titles_range:
#     for j in titles_range:
#         plt.text(j, i, round(similarity[i][j], 2),
#                  ha="center", va="center", color="w")
# plt.show()
