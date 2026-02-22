def predict_forgetting(model, input_features):
    probability = model.predict_proba(input_features)[0][1]
    return probability