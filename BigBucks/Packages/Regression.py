import pandas as pd
from sklearn.linear_model import LinearRegression

def Regression(data, y_name, x_name):
    x = data[[x_name]].values
    y = data[y_name]

    model = LinearRegression()

    model.fit(x,y)
    predict_y = model.predict(x)

    result = pd.DataFrame()
    result['x'] = data[x_name]
    result['y'] = predict_y

    return result
