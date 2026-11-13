"""2차원 벡터의 표시 책임만 담당하는 심화용 도구."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def save_vector_plot(coords: dict, filepath):
    path=Path(filepath);path.parent.mkdir(parents=True,exist_ok=True)
    fig,ax=plt.subplots(figsize=(6,4))
    for label,(x,y) in coords.items():
        ax.scatter(x,y,s=70)
        ax.annotate(label,(x,y),xytext=(5,5),textcoords="offset points")
    ax.set(xlabel="x1",ylabel="x2",title="Educational 2D vectors")
    ax.axhline(0,lw=.6);ax.axvline(0,lw=.6);ax.grid(alpha=.2)
    fig.tight_layout();fig.savefig(path,dpi=125);plt.close(fig)
