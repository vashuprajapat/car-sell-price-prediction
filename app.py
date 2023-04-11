from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():

    # year = request.form['year']
    # selling_price = request.form['selling_price']
    # km_driven = request.form['km_driven']
    # fuel = request.form['fuel']
    # seller_type = request.form['seller_type']
    # transmission = request.form['transmission']
    # owner = request.form['owner']

    # Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['year'])
        Kms_Driven=int(request.form['km_driven'])
        Kms_Driven2=np.log(Kms_Driven)
        owner = request.form['owner']
        owner_First_Owner=0
        owner_Fourth_Above_Owner=0
        owner_Second=0
        owner_third=0
        owner_Test=0

        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=0
        Fuel_Type_Cng=0
        Fuel_Type_Lpg=0
        Fuel_Type_Electric=0

        # Handel owner
        if(owner=='First Owner'):
            owner_First_Owner=0
        elif(owner=='Second Owner'):
            owner_Second=1
        elif(owner=='Third Owner'):
            owner_third=1
        elif(owner=='Fourth & Above Owner'):
            owner_Fourth_Above_Owner=1
        else:
            owner_Test=1
        
        # handel fueltype
        Fuel_Type=request.form['fuel']
        if(Fuel_Type=='Petrol'):
                Fuel_Type_Petrol=1
        elif(Fuel_Type=='Diesel'):
            Fuel_Type_Diesel=1
        elif(Fuel_Type=='CNG'):
            Fuel_Type_Cng=1
        elif(Fuel_Type=='LPG'):
            Fuel_Type_Lpg=1
        elif(Fuel_Type=='Electric'):
            Fuel_Type_Electric=1
        
        Year=2023-Year


        Seller_Type_Individual=0
        Seller_Type_Dealer=0
        Seller_Type_Trustmark=0


        Seller_Type=request.form['seller_type']
        if(Seller_Type=='Individual'):
            Seller_Type_Individual=1
        elif(Seller_Type=='Dealer'):
            Seller_Type_Dealer=1
        else:
            Seller_Type_Trustmark=1

        Transmission_Mannual=0
        Transmission_Automatic=0
        Transmission=request.form['transmission']
        if(Transmission=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Automatic=1
        
        prediction=model.predict([[Kms_Driven2,Year,Fuel_Type_Cng,Fuel_Type_Diesel,Fuel_Type_Electric, Fuel_Type_Lpg,Fuel_Type_Petrol,Seller_Type_Dealer,Seller_Type_Individual,Seller_Type_Trustmark,Transmission_Automatic,Transmission_Mannual,owner_First_Owner,owner_Fourth_Above_Owner,owner_Second,owner_Test,owner_third]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {} Rs approximately.".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)