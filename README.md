# Yelp Restaurants Recommendation System

Welcome to the Yelp Restaurants Recommendation System project! This system aims to provide personalized recommendations to users and predict user-business pairs based on their preferences and behavior using data mining techniques, Spark RDD, and collaborative filtering algorithms. 

# Note
The files **app.py** and **RecommendationSystem.py**, which house the primary Spark code and application logic, are securely stored within a **private repository** in accordance with the project requirements. This project serves as an extension of a previous course project, facilitating user interaction through a user-friendly interface. Users can conveniently select users and businesses, enabling them to view recommendation scores with ease

## Demo Video


## Features
- **XGBoost-Regressor based Recommendation**: Utilizes XGBoost (XGB) as the primary recommendation engine.
- **Collaborative Filtering**: Utilizes item-based collaborative filtering with Pearson Similarity to provide accurate recommendations by analyzing item similarities.
- **Hybrid Recommendation System**: Enhances recommendations through feature mining, achieving significant RMSE reduction from 1.09 to 0.9798.


## Techniques Used

- **Data Mining**: Extracts insights and patterns from very large Yelp dataset.
- **Spark RDD**: Utilizes Spark Resilient Distributed Datasets for parallel processing and efficient data manipulation.
- **Collaborative Filtering**: recommendations are made by identifying businesses that are similar to the businesses the user has interacted with or shown interest in.

## Results

The recommendation system demonstrates promising performance in predicting user-business ratings, with an RMSE reduction achieved through feature mining. The hybrid approach combining collaborative filtering and feature engineering enhances the accuracy of recommendations.

## Usage

1. **Setup**: Ensure you have Spark installed and configured in your environment.
2. **Data Preparation**: Load the Yelp restaurant dataset into your environment.
3. **Execution**: Integrate and execute the provided Spark code to generate recommendations.
4. **Web Interface**: Utilize `app.py` (stored in the private repository) to integrate the system into a web interface for user interaction.





## Contributors

- [Sharvari Kalgutkar]



