from flask import Flask, render_template,jsonify
import json
import pandas as pd
import pickle
import random
app = Flask(__name__)


with open('xgb.pkl', 'rb') as f:
    model=pickle.load(f)

with open('standard_scaler.pkl', 'rb') as g:
    scalar=pickle.load(g)

with open('data/business_reviews.json','r') as r:
     reviews_b=json.load(r)

with open('data/user_reviews.json','r') as r:
     reviews_u=json.load(r)

def cal_error_dist(ground_truth, model_final_dict_1):
      sum_0_1=0
      sum_1_2=0
      sum_2_3=0
      sum_3_4=0
      sum_4=0
      for k in model_final_dict_1.keys(): 
              diff=abs(ground_truth[k]-model_final_dict_1[k])
              if diff>=0 and diff<1:
                     sum_0_1+=1
              elif diff>=1 and diff<2:
                     sum_1_2+=1
              elif diff>=2 and diff<3:
                     sum_2_3+=1
              elif diff>=3 and diff<4:
                     sum_3_4+=1
              else:
                     sum_4+=1
      print(sum_0_1,sum_1_2,sum_2_3,sum_3_4,sum_4)
            
            
            
def error_d_val(l):
    id=l.split(',')
    return (id[1],id[0],float(id[2]))
def read_csv(l):
    id=l.split(',')
    return (id[0],(id[1],float(id[2])))

def read_csv_val(l):
    id=l.split(',')
    return (id[0],(id[1],))

def years_on_yelp(date):
    
    year=date.split('-')[0]
    date=2023-int(year)
    return date

def count_attributes(row_attr):
    if type(row_attr)==dict:
        return len(row_attr)
    else:
        return 0
    
    
def checkin(dct):
    sum=0
    for k,v in dct.items() :
        sum+=int(v)
    return sum

def user_sc_comp(row):
    sum=row["compliment_hot"]+row["compliment_more"]+row["compliment_profile"]+row["compliment_cute"]+row["compliment_list"]+row["compliment_note"]+row["compliment_plain"]+row["compliment_cool"]+row["compliment_funny"]+row["compliment_writer"]+row["compliment_photos"]
    return sum
def user_friends(row_attr):
    if row_attr=="None":
        return 0
    else: 
        return len(row_attr.split(","))

def general_mode_1(row_attr,attr):
    if type(row_attr)==dict:
          if attr in row_attr.keys():
                if row_attr[attr]=="True":
                    return 1
                else:
                    return 0
               
          else:
               return 1
    else:
               return 1
        

def general_mode_0(row_attr,attr):
    if type(row_attr)==dict:
          if attr in row_attr.keys():
                if row_attr[attr]=="True":
                    return 1
                else:
                    return 0
               
          else:
               return 0
    else:
               return 0
        
    


def score_noise(row_attr):
    if type(row_attr)==dict:
            if "NoiseLevel" in row_attr.keys():
                k="NoiseLevel"
                if row_attr[k]=='quiet':
                    score= 1
                elif row_attr[k]=='average':
                    score=0

                elif row_attr[k]=='loud':
                    score=-1
                else:
                    score=-2
            else:
                 score=0
    else:
        score=0
        
    return score

def score_b_parking(row_attr):
    if type(row_attr)==dict:
          if "BusinessParking" in row_attr.keys():
                

               if "True" in row_attr["BusinessParking"]:
                    return 1
               else: 
                    return 0
          else:
               return 1
    return 1

def price_range(row_attr):
    if type(row_attr)==dict:
          if "RestaurantsPriceRange2" in row_attr.keys():
                return int(row_attr["RestaurantsPriceRange2"])
          else:
               return 2
    else:
              return 2
      
def alcohol(row_attr):
    if type(row_attr)==dict:
          if "Alcohol" in row_attr.keys():
                if row_attr['Alcohol']=='full_bar': 
                    return 2
                elif row_attr['Alcohol']=='beer_and_wine':
                    return 1
                else:
                    return 0
          else:
               return 0
    else:
            return 0

def wifi(row_attr):
    if type(row_attr)==dict:
          if "WiFi" in row_attr.keys():
                if row_attr['WiFi']=='free': 
                    return 2
                elif row_attr['WiFi']=='paid':
                    return 1
                else:
                    return 0
          else:
               return 2
    else:
            return 2
        
def weekday_scr(row_attr):
    if type(row_attr) == dict:
        if "BestNights" in row_attr.keys():
            k = "BestNights"
            row_attr[k] = row_attr[k].replace("'", "\"") 
            row_attr[k]=row_attr[k].lower()
            
            day_dct = json.loads(row_attr[k])
            score=(
                int(day_dct.get('monday', 0)) +
                int(day_dct.get('tuesday', 0)) +
                int(day_dct.get('wednesday', 0)) +
                int(day_dct.get('thursday', 0)) +
                int(day_dct.get('friday', 0))
            )
            return score
        else:
            return 2
    else:
        return 2
    
def weekend_scr(row_attr):
    if type(row_attr) == dict:
        if "BestNights" in row_attr.keys():
            k = "BestNights"
            row_attr[k] = row_attr[k].replace("'", "\"") 
            row_attr[k]=row_attr[k].lower()
            
            day_dct = json.loads(row_attr[k])
            score=(
                int(day_dct.get('saturday', 0)) +
                int(day_dct.get('sunday', 0)) 
                
            )
            return score
        else:
            return 1
    else:
        return 1

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/user_data')
def user_data():
    with open('data/u.json', 'r') as f:
        users=json.load(f)
        print(users)
        return jsonify(users)
    
@app.route('/api/reviews')
def reviews():
    with open('data/review_train.json', 'r') as f:
        reviews=json.load(f)
        return jsonify(reviews)
    
@app.route('/api/business_data')
def bussiness_data():
    with open('data/b.json', 'r') as f:
        business=json.load(f)
        return jsonify(business)


@app.route('/predict/<user_id>/<business_id>')
def predict(user_id, business_id):
    # Dummy recommendation score calculation (you can replace this with your logic)
    with open('data/u.json', 'r') as f:
        users=json.load(f)
    user=users[int(user_id)]
    user_sel=users[int(user_id)]
    with open('data/b.json', 'r') as f:
        business=json.load(f)
    business_sel=business[int(business_id)]
    business=business[int(business_id)]
   

    business= (business['business_id'], business['stars'], business['review_count'], business['is_open'], count_attributes(business['attributes']),
               general_mode_1(business['attributes'],"BikeParking"),score_noise(business['attributes']), price_range(business['attributes']),
               alcohol(business['attributes']), wifi(business['attributes']),weekend_scr(business['attributes']), weekday_scr(business['attributes']),
               score_b_parking(business['attributes']),general_mode_1(business['attributes'],"BusinessAcceptsCreditCards") ,
               general_mode_1(business['attributes'],"GoodForKids"),general_mode_1(business['attributes'],"HasTV"),general_mode_0(business['attributes'],"OutdoorSeating"),
               general_mode_0(business['attributes'],"RestaurantsDelivery"),
               general_mode_1(business['attributes'],"RestaurantsGoodForGroups"), general_mode_0(business['attributes'],"RestaurantsReservations"),general_mode_1(business['attributes'],"RestaurantsTakeOut"),
               general_mode_1(business['attributes'],"Caters"),general_mode_0(business['attributes'],"DogsAllowed"),general_mode_0(business['attributes'],"DriveThru"),general_mode_1(business['attributes'],"RestaurantsTableService"),
               general_mode_1(business['attributes'],"WheelchairAccessible"),
               general_mode_0(business['attributes'],"BYOB"), general_mode_0(business['attributes'],"CoatCheck"),general_mode_0(business['attributes'],"Corkage"), general_mode_0(business['attributes'],"GoodForDancing"), 
               general_mode_1(business['attributes'],"HappyHour"),general_mode_0(business['attributes'],"ByAppointmentOnly"), general_mode_1(business['attributes'],"AcceptsInsurance"),general_mode_0(business['attributes'],"BusinessAcceptsBitcoin"))
    user=(user['user_id'], user['review_count'],years_on_yelp(user["yelping_since"] ),user['useful'], user['average_stars'],user['fans'] ,user_friends(user["friends"]),user_sc_comp(user))
    columns = ['business_id','user_id','user_review_count','yelping_since','useful','average_stars','fans','cnt_friends','comp_scr','stars','business_review_count','is_open','bike','score_attr','noise_score','price_range','alcohol','wifi','weekend_scr','weekday_scr','b_park','card','kids','tv','outseat','delivery','goodgroups','reserve','takeout','cater','dogs','drivethru','tableservice','wheelchair','byob','coat','corkage','dance','happyhour','appt','insurance','bitcoin']
    
    data=[business[0],user[0],user[1],user[2],user[3],user[4],user[5],user[6],user[7],business[1],business[2],business[3],business[5],business[4],business[6], business[7],business[8],business[9],business[10],business[11],business[12],business[13],business[14],business[15],business[16],business[17],business[18],business[19],business[20],business[21],business[22],business[23],business[24],business[25],business[26],business[27],business[28],business[29],business[30],business[31],business[32],business[33]]
    df = pd.DataFrame(columns=columns, data=[data])



    df_scale=df[['yelping_since','useful','fans','cnt_friends','comp_scr','business_review_count']]
    df.drop(['yelping_since','useful','fans','cnt_friends','comp_scr','business_review_count'],axis=1,inplace=True)
    df_scale = scalar.transform(df_scale)
    df_scale=pd.DataFrame(df_scale,columns=['yelping_since','useful','fans','cnt_friends','comp_scr','business_review_count'])
    df_scale=pd.concat([df,df_scale],axis=1)

    score=model.predict(df_scale.iloc[:,2:])
    dis_score=round(float(score[0]),1)
    score=json.dumps({'score':round(float(score[0]),1)})


    review_user_ls=[]
    for r in reviews_u:
         if r['user_id']==user_sel['user_id']:
              review_user_ls.append(r['text'])
    if len(review_user_ls)>5:
        review_user_ls=random.sample(review_user_ls,5)
   

    review_business_ls=[]
    for r in reviews_b:
         if r['user_id']==user_sel['user_id']:
              review_business_ls.append(r['text'])
    if len(review_business_ls)>5:
        review_business_ls=random.sample(review_business_ls,5)





    return render_template('score_page.html',dis_score=dis_score, recommendation_score=score, user=user_sel, business=business_sel, review_b=review_business_ls,review_u=review_user_ls)

def calculate_recommendation_score(user_id, business_id):
    # Implement your recommendation score calculation logic here
    # This is just a dummy example
    return f"Score for User {user_id} and Business {business_id}: {42}"



if __name__ == "__main__":
    app.run(debug=True)
