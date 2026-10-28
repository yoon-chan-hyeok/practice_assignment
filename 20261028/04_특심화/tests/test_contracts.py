"""수강생도 실행 가능한 계약 검사. TODO가 남아 있으면 실패하는 것이 정상입니다.
실행: 역할 폴더에서 python -m unittest discover -s tests -v
"""
from pathlib import Path
import sys,importlib.util,unittest
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from course_support import load_data,FEATURES,NUM,check_features,classification_folds
from model_support import candidates,numeric_cluster
from sklearn.metrics import f1_score,roc_auc_score
CACHE={}
def ex(number,level=1):
    key=(number,level)
    if key not in CACHE:
        folder=next(ROOT.glob(f'ex{number:02d}_*'));lev=next(folder.glob(f'{level:02d}_*'))
        spec=importlib.util.spec_from_file_location(f'exercise_{number}_{level}',lev/'main.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);CACHE[key]=mod
    return CACHE[key]

class InputContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=load_data()
    def test_split_sizes(self):self.assertEqual((len(self.d.X_train),len(self.d.X_valid),len(self.d.test_ids)),(60,20,20))
    def test_split_disjoint(self):
        a=set(self.d.X_train.index);b=set(self.d.X_valid.index);c=set(self.d.test_ids)
        self.assertFalse(a&b or a&c or b&c);self.assertEqual(len(a|b|c),100)
    def test_xy_alignment(self):
        self.assertTrue(self.d.X_train.index.equals(self.d.yc_train.index));self.assertTrue(self.d.X_valid.index.equals(self.d.yr_valid.index))
    def test_input_allowed(self):self.assertEqual(self.d.X_train.columns.tolist(),FEATURES)
    def test_missing_column(self):
        with self.assertRaises(ValueError):check_features(self.d.X_valid.drop(columns='priority'))
    def test_extra_target(self):
        with self.assertRaises(ValueError):check_features(self.d.X_valid.assign(failed=0))
    def test_infinite_value(self):
        x=self.d.X_valid.copy();x.iloc[0,0]=np.inf
        with self.assertRaises(ValueError):check_features(x)
    def test_duplicate_id(self):
        x=pd.concat([self.d.X_valid.iloc[:1]]*2)
        with self.assertRaises(ValueError):check_features(x)
    def test_fold_partition(self):
        seen=[]
        for a,b in classification_folds(self.d):
            self.assertEqual((len(a),len(b)),(48,12));self.assertFalse(set(a)&set(b));seen.extend(b)
        self.assertEqual(sorted(seen),list(range(60)))

class MetricsContracts(unittest.TestCase):
    def test_hand_matrix(self):
        r=ex(1).compute_metrics([0]*14+[1]*6,[0]*10+[1]*4+[0]*4+[1]*2)
        self.assertEqual([r[k] for k in ['TN','FP','FN','TP']],[10,4,4,2]);self.assertAlmostEqual(r['F1'],1/3)
    def test_zero_positive(self):
        r=ex(1).compute_metrics([0,0],[0,0]);self.assertEqual(r['positive_n'],0);self.assertEqual(r['F1'],0)
    def test_metrics_invalid(self):
        with self.assertRaises(ValueError):ex(1).compute_metrics([0,1],[0])
    def test_all_success_comparison(self):
        r=ex(1,2).compare_predictions([0]*14+[1]*6,{'all':np.zeros(20,dtype=int)}).iloc[0]
        self.assertAlmostEqual(r.Accuracy,.7);self.assertEqual(r.Recall,0)
    def test_cost_weight(self):
        r=ex(1,3).error_costs([0,1],{'a':[1,0]},{'case':(2,7)});self.assertEqual(r.iloc[0]['cost'],9)
    def test_roc_auc(self):
        curve,pairs,auc=ex(2).roc_and_pairs([0,0,1,1],[.1,.4,.35,.8]);self.assertAlmostEqual(auc,.75);self.assertEqual(pairs.credit.sum(),3)
    def test_auc_ties(self):
        _,pairs,auc=ex(2).roc_and_pairs([0,1],[.5,.5]);self.assertEqual(auc,.5);self.assertEqual(pairs.credit.sum(),.5)
    def test_threshold_cost(self):
        r=ex(2,2).threshold_table([0,0,1,1],[.1,.4,.35,.8]);self.assertEqual(r.cost.tolist(),[5,1])
    def test_threshold_equality(self):
        r=ex(2,2).threshold_table([0,1],[.5,.5],[.5]);self.assertEqual((r.iloc[0].FP,r.iloc[0].FN),(0,1))
    def test_single_class_auc(self):self.assertIsNone(ex(2,3).safe_auc([1,1],[.2,.8]))
    def test_auc_invalid(self):
        with self.assertRaises(ValueError):ex(2,3).safe_auc([0,1],[.2,np.nan])
    def test_rmse_hand(self):
        r=ex(3).regression_metrics([100,200,300,400],[100,200,300,480]);self.assertEqual(r,{'MAE_ms':20.,'RMSE_ms':40.})
    def test_rmse_invalid(self):
        with self.assertRaises(ValueError):ex(3).regression_metrics([],[])

class FeatureClusterContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=load_data()
    def test_feature_identity(self):
        x=self.d.X_valid.copy();before=x.copy(deep=True);out=ex(4).add_features(x)
        self.assertTrue(x.equals(before));self.assertTrue(x.index.equals(out.index));self.assertEqual(out.shape,(20,6))
    def test_feature_arithmetic(self):
        x=pd.DataFrame({'input_chars':[0.,99.,np.nan],'allowed_tools':[0.,2.,1.],'task_type':['qa']*3,'priority':['normal']*3})
        out=ex(4).add_features(x);self.assertAlmostEqual(out.log_input_chars.iloc[1],np.log(100));self.assertEqual(out.chars_per_slot.iloc[1],33)
        self.assertTrue(np.isnan(out.chars_per_slot.iloc[2]));self.assertEqual(out.log_input_chars.iloc[0],0)
    def test_feature_negative_rejected(self):
        x=self.d.X_valid.copy();x.iloc[0,0]=-1
        with self.assertRaises(ValueError):ex(4).add_features(x)
    def test_cluster_counts(self):
        p=ex(5).fit_clusters(self.d.X_train[NUM]);r=ex(5).profile(p)
        self.assertEqual(r.n.tolist(),[24,19,17]);self.assertEqual(r.n.sum(),60)
    def test_cluster_k_error(self):
        with self.assertRaises(ValueError):ex(5).fit_clusters(self.d.X_train[NUM],60)
    def test_predict_keeps_centers(self):
        p=numeric_cluster(self.d.X_train,3);before=p['cluster'].cluster_centers_.copy()
        x=pd.DataFrame({'input_chars':[200.,2200.],'allowed_tools':[1.,5.]});labels=ex(5,2).assign_new(p,x)
        self.assertEqual(labels.tolist(),[2,0]);self.assertTrue(np.array_equal(before,p['cluster'].cluster_centers_))
    def test_cluster_label_permutation(self):
        r=ex(5,3).compare_cluster_labels([0,0,1,1],[1,1,0,0]);self.assertEqual(r['ARI'],1);self.assertTrue(r['same_partition'])
    def test_exact_tie_rule(self):
        names=list(candidates());t=pd.DataFrame({'model':names[::-1],'CV_F1':[.5]*7,'valid_F1':range(7)})
        self.assertEqual(ex(6).choose_candidate(t),'Dummy')
    def test_cv_not_valid_selection(self):
        names=list(candidates());t=pd.DataFrame({'model':names,'CV_F1':[.1,.2,.3,.4,.5,.6,.61],'valid_F1':[1,0,0,0,0,0,0]})
        self.assertEqual(ex(6).choose_candidate(t),'Logistic_FE')

if __name__=='__main__':unittest.main(verbosity=2)
