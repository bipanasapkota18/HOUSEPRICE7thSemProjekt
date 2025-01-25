import pickle

with open(r'E:\HOuse_p\HOUSEPRICE7thSemProjekt\houseprice\prediction\best_rf_model.pkl', 'rb') as model_file:
    best_rf_model = pickle.load(model_file)
    print(type(best_rf_model))  # Ensure this is a valid RandomForest model

# with open(r'E:\HOuse_p\HOUSEPRICE7thSemProjekt\houseprice\prediction\scaler.pkl', 'rb') as scaler_file:
#     scaler = pickle.load(scaler_file)
#     print(type(scaler))  # Ensure this is a valid scaler object (e.g., StandardScaler)
