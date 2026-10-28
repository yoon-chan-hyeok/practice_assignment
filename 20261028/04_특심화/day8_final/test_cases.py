"""실습07/08 심화. 먼저 main.py 실행 후 `python test_cases.py`로 검사합니다."""
from pathlib import Path
import unittest,tempfile,shutil
import numpy as np
from data_io import load_data,check_features,NUM
from preprocessing import candidates,failure_scores
from feature_ops import add_features
from evaluate import classification_metrics,fold_statistics
from protocol import read_json,write_json,verify_lock
from main import fitted_snapshot
ROOT=Path(__file__).resolve().parent

def assert_missing_rejected(X):
    """[D8-P08] priority를 제거했을 때 ValueError가 나는지 검사합니다. 거부하지 않으면 AssertionError."""
    # TODO D8-P08: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-P08")

def assert_lock_change_rejected(out):
    """[D8-P09] outputs 임시복사본의threshold만.3으로변경한뒤verify_lock이거부하는지검사.
    원본파일을수정하지않습니다. 실패를올바르게감지하면True를반환합니다.
    """
    # TODO D8-P09: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-P09")

class ProjectChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.dev=load_data(ROOT/'data')
    def test_missing_column(self):self.assertTrue(assert_missing_rejected(self.dev.X_valid))
    def test_lock_change(self):self.assertTrue(assert_lock_change_rejected(ROOT/'outputs'))
    def test_fold_statistics(self):self.assertTrue(fold_statistics(self.dev).own_fit.all())
    def test_new_category_missing_values(self):
        p=candidates()['Logistic_FE'].fit(self.dev.X_train,self.dev.yc_train)
        x=self.dev.X_valid.iloc[:2].copy();x['task_type']='translation';x['priority']='urgent';x.loc[:,NUM]=np.nan
        before=fitted_snapshot(p);z=p[:-1].transform(check_features(x));score=failure_scores(p,x)
        self.assertEqual(z.shape,(2,10));self.assertTrue(np.isfinite(z).all());self.assertTrue(np.isfinite(score).all())
        self.assertEqual(before,fitted_snapshot(p))
    def test_single_class_auc(self):
        r=classification_metrics([0,0,0],[0,0,0],[.1,.2,.3]);self.assertIsNone(r['ROC_AUC']);self.assertEqual(r['positive_n'],0)
    def test_copy_and_order(self):
        x=self.dev.X_valid.copy();before=x.copy(deep=True);out=add_features(x)
        self.assertTrue(x.equals(before));self.assertTrue(out.index.equals(x.index))
    def test_negative_input(self):
        x=self.dev.X_valid.copy();x.iloc[0,x.columns.get_loc('input_chars')]=-1
        with self.assertRaises(ValueError):check_features(x)
    def test_probability_validation(self):
        with self.assertRaises(ValueError):classification_metrics([0,1],[0,1],[.1,1.5])
if __name__=='__main__':unittest.main(verbosity=2)
