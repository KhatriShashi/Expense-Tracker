from flask import Flask,request,jsonify
from uuid import uuid1,uuid4
import os,json,pytz
from datetime import date,datetime
import pandas as pd

db={}

db_filename="rohit.json"

#check whether db.josn exists in the directory or not
if os.path.exists(db_filename):
    with open(db_filename,"r") as f:
        db=json.load(f)
else:
    accessKey=str(uuid1())
    secretKey=str(uuid4())
    item_types=[
        "Food","Beverages","Clothing","Stationaries","Wearables","Electronics Accessories"
    ]
    db={
        "accessKey":accessKey,
        "secretKey":secretKey,
        "item_type":item_types,
        "users":[]
    }
    with open(db_filename,"w") as f:
        json.dump(db,f,indent=4)

app=Flask(__name__)

# user sign up
@app.route('/signup',methods=['POST'])

def signup():
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        username=request.form['username']

        userDict={
            "name":name,
            "email":email,
            "password":password,
            "username":username,
            "purchases": {}
        }
        email_list = []
        for element in db["users"]:
            email_list.append(element["email"])

        if(len(db["users"])) == 0 or userDict["email"] not in email_list:
            db["users"].append(userDict)
            with open(db_filename,"r+") as f:
                f.seek(0)
                json.dump(db,f,indent=4)
            return "User added successfully"
        else:
            return "User already exitsts"
    return "Error:Trying to access endpoint with wrong method"


#user sing in
@app.route('/login',methods=["POST"])

def login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        user_idx=None
        for user in db["users"]:
            if user["email"]==email and user["password"]==password:
                user_idx=db["users"].index(user)

                response={
                    "message":"logged in successfully",
                    "user_idx":user_idx
                }
                return response
            else:
                continue
        return "Wrong email or password!Please try again:"

#add purchases
@app.route('/add_purchase',methods=["POST"])
def addpurchase():
    if request.method=="POST":
        user_idx=int(request.form["user_index"])
        item_name=request.form["item_name"]
        item_type=request.form["item_type"]
        item_price=request.form["item_price"]

        curr_date=str(date.today())
        curr_time=str(datetime.now(pytz.timezone("Asia/Kolkata")))
        itemDict={
            "item_name":item_name,
            "item_type":item_type,
            "item_price":item_price,
            "purchase_time":curr_time
        }
        if(user_idx<len(db["users"]) and user_idx>=0):
            if len(db["users"][user_idx]["purchases"])==0 or curr_date not in list(db["users"][user_idx]["purchases"].keys()):
            #if there are no purchases user has done for the day
                db["users"][user_idx]["purchases"][curr_date]=[]
                db["users"][user_idx]["purchases"][curr_date].append(itemDict)
                with open(db_filename,"r+") as f:
                    f.seek(0)
                    json.dump(db,f,indent=4)
                return "item added successfully"
            else:
                db["users"][user_idx]["purchases"][curr_date].append(itemDict)
                with open(db_filename,"r+") as f:
                    f.seek(0)
                    json.dump(db,f,indent=4)
                return "item added successfully"
        return "Some error occured!Unable to add item"

@app.route("/get_all_purchases_for_today",methods=["GET"])
def get_all_purchases_for_today():
    user_idx=int(request.args["user_index"])
    print("user Index=",user_idx)
    curr_date=str(date.today())
    list_of_purchases=db["users"][user_idx]["purchases"][curr_date]
    purchasedates=list(db["users"][user_idx]["purchases"].keys())
    if(curr_date in purchasedates):
        return jsonify(purchases_for_today=list_of_purchases)
    else:
        return jsonify(message="Date Not found")


@app.route("/get_purchases",methods=["GET"])
def get_purchases():
    data=request.json
    user_index=data["user_index"]
    start_date=data["start_date"]
    end_date=data["end_date"]

    dates=pd.date_range(start_date,end_date)
    dates_in_db=list(db["users"][user_index]["purchases"].keys())

    purchaseDict={}
    for dt in dates_in_db:
        if dt in dates:
            purchaseDict[dt]=db["users"][user_index]["purchases"][dt]
        else:
            continue
    return purchaseDict


if __name__=='__main__':
    app.run(host='0.0.0.0',port='5000',debug=True)