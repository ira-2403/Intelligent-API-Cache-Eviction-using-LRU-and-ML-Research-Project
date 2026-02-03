import pandas as pd 
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from backend.ml.features import create_features
df=pd.read_csv("backend/data/request_logs.csv")
df=create_features(df)
df["reuse_soon"]=(df["url_freq"]>0).astype(int)
X=df[["url_freq","time_diff","cache_hit","response_time_ms","data_size"]].fillna(0)
y=df["reuse_soon"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(X_train,y_train)
y_pred=model.predict(X_train)
y_pred=model.predict(X_test)
print(classification_report(y_test,y_pred))
joblib.dump(model,"backend/ml/cache_reuse_model.pkl")
print("Model trained and saved successfully.")