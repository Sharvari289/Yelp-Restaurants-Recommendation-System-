
from pyspark import  SparkContext
import json
import pandas as pd
from xgboost import XGBRegressor
import sys
from sklearn.preprocessing import StandardScaler

folder=sys.argv[1]
test=sys.argv[2]
out=sys.argv[3]
      
    
sc = SparkContext.getOrCreate()
sc.setLogLevel("WARN")

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

lines=sc.textFile(folder+"/yelp_train.csv")
col=lines.first()
train_data=lines.filter(lambda l: l!=col).map(lambda l:read_csv(l))


b = sc.textFile(folder+'/business.json')
b=b.map(lambda row: json.loads(row)).map(lambda row: (row['business_id'], (row['stars'], row['review_count'], row['is_open'], count_attributes(row['attributes']),general_mode_1(row['attributes'],"BikeParking"),score_noise(row['attributes']), price_range(row['attributes']),alcohol(row['attributes']), wifi(row['attributes']),weekend_scr(row['attributes']), weekday_scr(row['attributes']),score_b_parking(row['attributes']),general_mode_1(row['attributes'],"BusinessAcceptsCreditCards") ,general_mode_1(row['attributes'],"GoodForKids"),general_mode_1(row['attributes'],"HasTV"),general_mode_0(row['attributes'],"OutdoorSeating"),general_mode_0(row['attributes'],"RestaurantsDelivery"),general_mode_1(row['attributes'],"RestaurantsGoodForGroups"), general_mode_0(row['attributes'],"RestaurantsReservations"),general_mode_1(row['attributes'],"RestaurantsTakeOut"),general_mode_1(row['attributes'],"Caters"),general_mode_0(row['attributes'],"DogsAllowed"),general_mode_0(row['attributes'],"DriveThru"),general_mode_1(row['attributes'],"RestaurantsTableService"),general_mode_1(row['attributes'],"WheelchairAccessible"),general_mode_0(row['attributes'],"BYOB"), general_mode_0(row['attributes'],"CoatCheck"),general_mode_0(row['attributes'],"Corkage"), general_mode_0(row['attributes'],"GoodForDancing"), general_mode_1(row['attributes'],"HappyHour"),general_mode_0(row['attributes'],"ByAppointmentOnly"), general_mode_1(row['attributes'],"AcceptsInsurance"),general_mode_0(row['attributes'],"BusinessAcceptsBitcoin")     )))
u = sc.textFile(folder+'/user.json')
u=u.map(lambda row: json.loads(row)).map(lambda row: (row['user_id'], (row['review_count'],years_on_yelp(row["yelping_since"] ),row['useful'], row['average_stars'],row['fans'] ,user_friends(row["friends"]),user_sc_comp(row)    )))
u_train= train_data.leftOuterJoin(u).map(lambda row:(row[1][0][0] ,(row[0], row[1][1][0], row[1][1][1], row[1][1][2], row[1][1][3], row[1][1][4],row[1][0][1],row[1][1][5],row[1][1][6])))
u_b_train=u_train.leftOuterJoin(b).map(lambda row:(row[0],row[1][0][0],row[1][0][1],row[1][0][2],row[1][0][3],row[1][0][4],row[1][0][5],row[1][0][7],row[1][0][8],row[1][1][0],row[1][1][1],row[1][1][2],row[1][1][3],row[1][1][4],row[1][1][5],row[1][1][6],row[1][1][7],row[1][1][8],row[1][1][9],row[1][1][10],row[1][1][11],row[1][1][12],row[1][1][13],row[1][1][14],row[1][1][15],row[1][1][16],row[1][1][17],row[1][1][18],row[1][1][19],row[1][1][20],row[1][1][21],row[1][1][22],row[1][1][23],row[1][1][24],row[1][1][25],row[1][1][26],row[1][1][27],row[1][1][28],row[1][1][29],row[1][1][30],row[1][1][31],row[1][1][32],row[1][0][6])).collect()
train_set = pd.DataFrame(u_b_train, columns = ['business_id','user_id','user_review_count','yelping_since','useful','average_stars','fans','cnt_friends','comp_scr','stars','business_review_count','is_open','bike','score_attr','noise_score','price_range','alcohol','wifi','weekend_scr','weekday_scr','b_park','card','kids','tv','outseat','delivery','goodgroups','reserve','takeout','cater','dogs','drivethru','tableservice','wheelchair','byob','coat','corkage','dance','happyhour','appt','insurance','bitcoin','rating'])


train_set.drop(['user_id', 'business_id'], axis=1, inplace=True)
X_train=train_set.drop('rating',axis=1)
y_train=train_set['rating']


val_data=sc.textFile(test)
col=lines.first()
val_data=val_data.filter(lambda l: l!=col).map(lambda l:read_csv_val(l))
u_val= val_data.leftOuterJoin(u).map(lambda row:(row[1][0][0] ,(row[0], row[1][1][0], row[1][1][1], row[1][1][2], row[1][1][3], row[1][1][4],row[1][1][5],row[1][1][6])))

u_b_val=u_val.leftOuterJoin(b).map(lambda row:(row[0],row[1][0][0],row[1][0][1],row[1][0][2],row[1][0][3],row[1][0][4],row[1][0][5],row[1][0][6],row[1][0][7],row[1][1][0],row[1][1][1],row[1][1][2],row[1][1][3],row[1][1][4],row[1][1][5],row[1][1][6],row[1][1][7],row[1][1][8],row[1][1][9],row[1][1][10],row[1][1][11],row[1][1][12],row[1][1][13],row[1][1][14],row[1][1][15],row[1][1][16],row[1][1][17],row[1][1][18],row[1][1][19],row[1][1][20],row[1][1][21],row[1][1][22],row[1][1][23],row[1][1][24],row[1][1][25],row[1][1][26],row[1][1][27],row[1][1][28],row[1][1][29],row[1][1][30],row[1][1][31],row[1][1][32])).collect()

val_set = pd.DataFrame(u_b_val, columns = ['business_id','user_id','user_review_count','yelping_since','useful','average_stars','fans','cnt_friends','comp_scr','stars','business_review_count','is_open','bike','score_attr','noise_score','price_range','alcohol','wifi','weekend_scr','weekday_scr','b_park','card','kids','tv','outseat','delivery','goodgroups','reserve','takeout','cater','dogs','drivethru','tableservice','wheelchair','byob','coat','corkage','dance','happyhour','appt','insurance','bitcoin'])
X_val=val_set.drop(['user_id', 'business_id'], axis=1)

X_train_scale=X_train[['yelping_since','useful','fans','cnt_friends','comp_scr','business_review_count']]
X_train.drop(['yelping_since','useful','fans','cnt_friends','comp_scr','business_review_count'],axis=1,inplace=True)

X_val_scale=X_val[['yelping_since','useful','fans','cnt_friends','comp_scr','business_review_count']]
X_val.drop(['yelping_since','useful','fans','comp_scr','cnt_friends','business_review_count'],axis=1,inplace=True)
scalar = StandardScaler()

scalar.fit(X_train_scale)
X_train_scale = scalar.transform(X_train_scale)
X_val_scale = scalar.transform(X_val_scale)

X_val_scale=pd.DataFrame(X_val_scale,columns=['yelping_since','useful','fans','cnt_friends','comp_scr','business_review_count'])
X_train_scale=pd.DataFrame(X_train_scale,columns=['yelping_since','useful','fans','cnt_friends','comp_scr','business_review_count'])

X_train=pd.concat([X_train,X_train_scale],axis=1)
X_val=pd.concat([X_val,X_val_scale],axis=1)



xgb = XGBRegressor(nthread=-1, eval_metric = "rmse", n_estimators=2010, learning_rate=0.1, subsample=0.8)
xgb.fit( X_train,y_train)
pred_train = xgb.predict(X_train)
pred_val=xgb.predict(X_val)

model_final_dict_1={}
for index, row in val_set.iterrows():
    model_final_dict_1[(row['business_id'],row['user_id'])]=pred_val[index]

final_dict = {}
final_dict=model_final_dict_1

with open(out, 'w') as f:
  f.write("user_id, business_id, prediction\n")
  for key,val in final_dict.items():
    f.write(str(key[1]) + "," + str(key[0]) + "," + str(val) + "\n")
    
                   

              
                     


