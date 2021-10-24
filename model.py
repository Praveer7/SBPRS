# import libraties
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


class Recommendation:
    
    def __init__(self):
        self.data = pickle.load(open('pickle/processed_data.pkl','rb'))
        self.user_final_rating = pickle.load(open('pickle/user_final_rating.pkl','rb'))
        self.model = pickle.load(open('pickle/logistic_regression.pkl','rb'))
        self.raw_data = pd.read_csv("dataset/sample30.csv")
        self.data = pd.concat([self.raw_data[['id','name','brand','categories','manufacturer']],self.data], axis=1)
        
        
    def getTopProducts(self, user):
        items = self.user_final_rating.loc[user].sort_values(ascending=False)[0:20].index
        features = pickle.load(open('pickle/features.pkl','rb'))
        vectorizer = TfidfVectorizer(vocabulary = features)
        temp=self.data[self.data.id.isin(items)]
        X = vectorizer.fit_transform(temp['Review'])
        temp=temp[['id']]
        temp['prediction'] = self.model.predict(X)
        temp['prediction'] = temp['prediction'].map({'Postive':1,'Negative':0})
        temp=temp.groupby('id').sum()
        temp['positive_percent']=temp.apply(lambda x: x['prediction']/sum(x), axis=1)
        final_list=temp.sort_values('positive_percent', ascending=False).iloc[:5,:].index
        return self.data[self.data.id.isin(final_list)][['id', 'brand',
                              'categories', 'manufacturer', 'name']].drop_duplicates().to_html(index=False)
    
        
        

