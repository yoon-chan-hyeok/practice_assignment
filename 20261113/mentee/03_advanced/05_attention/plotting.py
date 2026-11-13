"""Attention 가중치의 Heatmap 시각화: 계산 함수와 분리."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def save_attention_heatmap(weights,filepath):
    path=Path(filepath);path.parent.mkdir(parents=True,exist_ok=True)
    fig,ax=plt.subplots(figsize=(4.8,4))
    heat=ax.imshow(weights.detach().cpu().numpy(),vmin=0,vmax=1,cmap="Blues")
    ax.set(xticks=range(3),yticks=range(3),xlabel="Key index",ylabel="Query index")
    for i in range(3):
        for j in range(3):
            ax.text(j,i,f"{weights[i,j]:.2f}",ha="center",va="center")
    fig.colorbar(heat,ax=ax);fig.tight_layout()
    fig.savefig(path,dpi=130);plt.close(fig)
