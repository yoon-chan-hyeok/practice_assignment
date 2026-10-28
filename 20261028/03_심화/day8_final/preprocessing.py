"""제공 모듈: 전처리 구성과 후보 설정만 담습니다. import만으로 학습하지 않습니다."""
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from xgboost import XGBClassifier
from features import add_features

FEATURES = ["input_chars", "allowed_tools", "task_type", "priority"]
NUM, CAT = FEATURES[:2], FEATURES[2:]
DERIVED = ["log_input_chars", "chars_per_slot"]

def build(estimator, derived=False, scale=True):
    """매번 학습 전 상태의 Pipeline을 만듭니다. 결측·범주 처리는 전날과 같습니다."""
    numbers = NUM + DERIVED if derived else NUM
    numeric = [("imputer", SimpleImputer(strategy="median", keep_empty_features=True))]
    if scale:
        numeric.append(("scaler", StandardScaler()))
    category = Pipeline([("imputer", SimpleImputer(strategy="most_frequent", keep_empty_features=True)),
                         ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
    pre = ColumnTransformer([("num", Pipeline(numeric), numbers), ("cat", category, CAT)])
    steps = [("features", FunctionTransformer(add_features, validate=False))] if derived else []
    return Pipeline(steps + [("pre", pre), ("model", clone(estimator))])

# 후보·파라미터는 test 확인 전에 고정합니다. 순서가 동점 처리 순서입니다.
CANDIDATES = {
    "Dummy": build(DummyClassifier(strategy="most_frequent")),
    "Logistic": build(LogisticRegression(C=1, max_iter=1000)),
    "KNN3": build(KNeighborsClassifier(n_neighbors=3)),
    "Tree": build(DecisionTreeClassifier(max_depth=3, min_samples_leaf=3, random_state=42), scale=False),
    "Forest": build(RandomForestClassifier(n_estimators=100, max_depth=4, min_samples_leaf=2,
                                          max_features="sqrt", random_state=42, n_jobs=1), scale=False),
    "XGB": build(XGBClassifier(n_estimators=80, max_depth=2, learning_rate=0.05,
                              min_child_weight=1, subsample=0.8, colsample_bytree=1.0, reg_lambda=1.0,
                              objective="binary:logistic", eval_metric="logloss", tree_method="hist",
                              device="cpu", random_state=42, n_jobs=1), scale=False),
    "Logistic_FE": build(LogisticRegression(C=1, max_iter=1000), derived=True),
}
