import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from common import Page, Similarity
import numpy as np
import re


def build_abbreviation(input: str):
    expr = re.findall(r"\b\w", input)
    return "".join(word.upper() for word in expr)


engine = create_engine("sqlite:///data.db")
session = Session(engine)

pages = session.query(Page).all()
pages_abbrevs = [build_abbreviation(page.title) for page in pages]

sims_vals = []
for first in pages:
    sims = session.query(Similarity) \
                  .filter(Similarity.first == first.id) \
                  .all()
    vals = []
    for sim in sims:
        val = round(sim.similarity, 2)
        vals.append(val)
    sims_vals.append(vals)

nlen = len(pages)

fig, ax = plt.subplots()
fig.patch.set_visible(False)
ax.axis("off")
ax.axis("tight")

pages_names = [[abbrev] for abbrev in pages_abbrevs]
for i, page in enumerate(pages):
    pages_names[i].append(page.title)

table = ax.table(cellText=pages_names,
                 colLabels=["Abkürzung", "Artikelname"],
                 loc="center", cellLoc="center")
table.auto_set_font_size(False)
table.set_fontsize(12)
table.auto_set_column_width(col=[0, 1])
table.scale(1.5, 1.5)
fig.tight_layout()
fig.savefig("fig/table.png", dpi=150)

fig, ax = plt.subplots()
heatmap = ax.imshow(sims_vals, cmap="bwr")
fig.colorbar(heatmap)

ticks = np.arange(nlen)
ax.set_xticks(ticks,
              labels=pages_abbrevs,
              rotation=45,
              ha="right")
ax.set_yticks(ticks,
              labels=pages_abbrevs)

# for i in range(nlen):
#     for j in range(nlen):
#         ax.text(j, i, sims_vals[i][j],
#                 ha="center", va="center",
#                 color="black")

ax.set_title("Ähnlichkeit nach Artikelabkürzung")
fig.tight_layout()
fig.savefig("fig/heatmap.png", dpi=150)
