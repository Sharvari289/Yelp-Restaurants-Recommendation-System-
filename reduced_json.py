import json
with open('data/review_formatted.json','r') as r:
    data=json.load(r)


user_id=["OQT9DjfBrzrwOEdVJjuYIA","YgavGxfAdjhkkbwlAY_9ZQ","UGW-9bbBEB3eP1o6mWD_WA","FNyEz_Tx1EBFqIn0s-7kVw","rPbIVGuIjmxHDw8ChhTsrw","n_TY6rd1wXZBczBaOaK6Rw","TQANOs9Q5DpFJgE-BzPi_Q","MgNkhX_twE5Gp9BK-yWZPQ","jEBySjq6tgL-_R3P7LHq0w","TYiDRwfIUBEos45ERdzeAw"]
business_id=["JQOg5iKV-c8e3b6ty8Jjbg","yhoCIkTwHihWejVqGYZ4rw","ZQyCqgVF-nzhG4BGh9NLQg","qLUr-ZPGVJejkSXIUenw6w","-PL-4fFYPYrOjnNd0lO4Lg","LtbuQJJn9pRhNf9BqGuNBQ","vOMDU31gdylrzBhAKC9QbA","gAJVjc0VUUtuBm_TSzanNA","qv88BZd88Va7ZuMOkzbUUQ","ExtP8z3SVyut_RICc9i_DA"]
final_user=[]
final_business=[]
for i in data:
    print(i['user_id'])
    if i['user_id'] in user_id:
        print(i['user_id'])
        final_user.append(i)
    if i['business_id'] in business_id:
        final_business.append(i)


with open('data/user_reviews.json', 'w') as outfile:
    json.dump(final_user, outfile)

with open('data/business_reviews.json', 'w') as outfile:
    json.dump(final_business,outfile)