import numpy as np, pandas as pd, pickle
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

rng = np.random.default_rng(42)
# location: PKR per square meter (approx base rate)
LOC = {"DHA Islamabad":260000,"Bahria Town Rawalpindi":170000,"F-10 Islamabad":330000,
       "Gulberg Lahore":280000,"DHA Lahore":300000,"Johar Town Lahore":190000,
       "Clifton Karachi":270000,"Gulshan-e-Iqbal Karachi":150000,"Saddar Rawalpindi":130000,
       "Satellite Town Rawalpindi":150000,"Hayatabad Peshawar":120000}
n = 6000
loc = rng.choice(list(LOC), n)
area = rng.uniform(60, 600, n)
bed = np.clip((area/55 + rng.normal(0,1,n)).round(),1,10).astype(int)
bath = np.clip((bed*0.8 + rng.normal(0,0.7,n)).round(),1,9).astype(int)
kitchen = np.clip((1 + (area>250)*rng.integers(0,2,n)).astype(int),1,3)
tv = np.clip((1 + (area>200)*rng.integers(0,2,n)).astype(int),0,3)
base = np.array([LOC[l] for l in loc]) * area
price = base*(1+0.03*(bed-3)+0.025*(bath-2)+0.02*(kitchen-1)+0.02*tv) * rng.normal(1,0.07,n)
df = pd.DataFrame(dict(bedrooms=bed,bathrooms=bath,kitchens=kitchen,tv_lounges=tv,
                       area_sqm=area.round(1),location=loc,price=price.round(-3)))
df.to_csv("house_data.csv",index=False)

X, y = df.drop(columns="price"), df["price"]
Xtr,Xte,ytr,yte = train_test_split(X,y,test_size=0.2,random_state=1)
pre = ColumnTransformer([("loc",OneHotEncoder(handle_unknown="ignore"),["location"])],remainder="passthrough")
model = Pipeline([("pre",pre),("gb",GradientBoostingRegressor(n_estimators=400,max_depth=4,learning_rate=0.05,random_state=1))])
model.fit(Xtr,ytr)
p = model.predict(Xte)
print("R2:",round(r2_score(yte,p),3)," MAE (PKR):",int(mean_absolute_error(yte,p)))
with open("house_price_model.pkl","wb") as f:
    pickle.dump({"model":model,"locations":sorted(LOC)},f)
