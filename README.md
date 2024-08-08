# Singapore-Resale-Flat-Price-Prediction

This project aims to develop a machine learning model to predict the resale prices of flats in Singapore. The model is deployed as a user-friendly web application that allows users to input specific details about a flat and receive an estimated resale value.

## Motivation
The resale flat market in Singapore is highly competitive, and it can be challenging to accurately estimate the resale value of a flat. Many factors influence resale prices, including location, flat type, floor area, and lease duration. This predictive model aims to assist potential buyers and sellers in making informed decisions by providing an estimated resale price based on these factors.

## Features
### Data Collection & Preprocessing:

Collected historical resale flat transaction data from the Singapore Housing and Development Board (HDB) covering the years 1990 to the present.
Preprocessed the data to clean and structure it for machine learning tasks.
### Feature Engineering:

Extracted and engineered features such as town, flat type, storey range, floor area, flat model, and lease commence date.
Created additional features to enhance model accuracy.
### Model Selection & Training:

Selected and trained various regression models, including linear regression, decision trees, and random forests.
Used a portion of the dataset for training and another portion for validation.
### Model Evaluation:

Evaluated the model using metrics such as Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and R² Score.
