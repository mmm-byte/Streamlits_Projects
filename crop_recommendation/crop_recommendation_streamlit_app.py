import pandas as pd
import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt

model = pickle.load(open('classifier.pkl','rb'))

b = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]

a = ['Apple','Banana','blackgram','chickpea','coconut','coffee',
     'cotton','grapes','jute','kidney beans','lentil','maize','mango',
     'moth beans','mung bean','muskmelon','orange','papaya','pigeonpeas',
     'pomegranate','Rice','Watermelon']

a = pd.DataFrame(a,columns=['label'])
b = pd.DataFrame(b,columns=['encoded'])
classes = pd.concat([a,b],axis=1).sort_values('encoded').set_index('label')

def predict(n,p,k,temp,humi,ph,rain):
    data=[[n,p,k,temp,humi,ph,rain]]
    pred = model.predict(data)
    
    #fetching the label for given encoded value
    for i in range(0,len(classes)):
        if(classes.encoded[i]==pred):
            output = classes.index[i].upper()
    return output

def predict_proba(n,p,k,temp,humi,ph,rain):
    data=[[n,p,k,temp,humi,ph,rain]]
    pred = model.predict_proba(data)
    pred = pd.DataFrame(data = np.round(pred.T*100,2), index=classes.index,columns=['predicted_values'])
    high = pred.predicted_values.nlargest(5)
    return high

def main():
    b1, titl, b2 = st.columns([1,5,1])
    titl.title('Crop Recommendation')
    st.sidebar.header('Enter the details')
    n = st.sidebar.number_input('Nitrogen(N) value in soil',value=1)
    p = st.sidebar.number_input('Phosphorous(P) value in soil',value=1)
    k = st.sidebar.number_input('Potassium(K) value in soil',value=1)
    temp = st.sidebar.number_input('Temperature in degree censius',value=1.0)
    ph = st.sidebar.number_input('PH value',value=1.0)
    humi = st.sidebar.number_input('Humidity in %',value=1)
    rain = st.sidebar.number_input('Rain Fall in mm',value=1.0)
    

    if st.button('Predict'):
        prediction = predict(n,p,k,temp,humi,ph,rain)
        b5, res, b6 = st.columns([1,5,1])
        res.header('Recommended Crop : {}'.format(prediction))

    if st.checkbox('Charts'):
        b3, res, b4 = st.columns([1,5,1])
        st.header('Top 5 recommended Crops')
        pred1 = predict_proba(n,p,k,temp,humi,ph,rain)
        
        # Use st.pyplot with clear_figure=True to clear previous plots
        fig, axes = plt.subplots()
        axes.pie(x=pred1,autopct='%1.1f%%',labels=pred1.index,explode=(0.1, 0, 0, 0, 0),shadow=True,startangle=90)
        st.pyplot(fig, clear_figure=True)
        
if __name__=='__main__':
    main()

