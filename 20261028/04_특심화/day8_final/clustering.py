"""제공 코드: 실습05의 결과를 재사용합니다. 정답을 받지 않는 독립 탐색 활동입니다."""
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score
from data_io import NUM
from preprocessing import numeric_cluster

def cluster_analysis(X_train):
    profile=None;scores=[];assignments=None
    for k in [2,3,4]:
        p=numeric_cluster(X_train,k);z=p[:-1].transform(X_train[NUM]);km=p['cluster']
        scores.append({'K':k,'inertia_standardized_squared':float(km.inertia_),
            'silhouette':float(silhouette_score(z,km.labels_)),'fit_n':len(X_train),'scope':'train60_numeric2_no_y'})
        if k==3:
            centers=p['scaler'].inverse_transform(km.cluster_centers_)
            profile=pd.DataFrame({'cluster':range(3),'n':np.bincount(km.labels_,minlength=3),
                'center_input_chars':centers[:,0],'center_allowed_tools':centers[:,1]})
            assignments=pd.DataFrame({'request_id':X_train.index,'cluster':km.labels_})
    return profile,pd.DataFrame(scores),assignments
