
class Task2:

    import pandas as pd
    weather = pd.read_csv("/content/drive/MyDrive/Weather_dataset/BerlinGermany.csv", index_col="datetime")

    weather

    null_pct = weather.apply(pd.isnull).sum()/weather.shape[0]
    null_pct

    valid_columns = weather.columns[null_pct < .03]

    valid_columns

    weather.apply(lambda x: (x == 9999).sum())

    weather.dtypes

    weather.index

    weather.index = pd.to_datetime(weather.index)

    weather.index.year.value_counts().sort_index( )

    weather ["tempmax"].plot()

    weather["target"] = weather.shift(-1)["tempmax"]

    weather

    weather = weather.ffill()
    weather

    weather.corr()

    from sklearn.linear_model import Ridge
    rr = Ridge(alpha=.1)

    predictors = weather.columns[~weather.columns.isin(["target", "name", "station","preciptype","sunrise","sunset","conditions", "description", "icon","stations"])]

    predictors

    def backtest(weather, model, predictors, start=30, step=10):
        all_predictions = []

        for i in range(start, weather.shape[0], step):
            train = weather.iloc[:i,:]
            test = weather.iloc[i:(i+step),:]

            model.fit(train[predictors], train["target"])

            preds = model.predict(test[predictors])
            preds = pd.Series(preds, index=test.index)
            combined = pd.concat([test["target"], preds], axis=1)
            combined.columns = ["actual", "prediction"]
            combined["diff"] = (combined["prediction"] - combined["actual"]).abs()

            all_predictions.append(combined)
        return pd.concat(all_predictions)

    weather= weather.fillna(0)

    predictions = backtest(weather, rr, predictors)

    predictions

    from sklearn.metrics import mean_absolute_error, mean_squared_error

    mean_absolute_error(predictions["actual"], predictions["prediction"])

    predictions["diff"].mean()

    pd.Series(rr.coef_, index=predictors)

    def pct_diff(old, new):
        return (new - old) / old

    def compute_rolling(weather, horizon, col):
        label = f"rolling_{horizon}_{col}"
        weather[label] = weather[col].rolling(horizon).mean()
        weather[f"{label}_pct"] = pct_diff(weather[label], weather[col])
        return weather

    rolling_horizons = [3, 10]
    for horizon in rolling_horizons:
        for col in ["tempmax", "tempmin", "precip"]:
            weather = compute_rolling(weather, horizon, col)

    weather

    weather = weather.iloc[10:,:]

    weather

    weather = weather.fillna(0)

    def calculate_expanding_mean(column):
        return column.expanding(1).mean()

    columns_to_process = ["tempmax", "tempmin", "precip"]

    for col in columns_to_process:
        month_avg_col_name = f"month_avg_{col}"
        day_avg_col_name = f"day_avg_{col}"

        weather[month_avg_col_name] = weather.groupby(weather.index.month)[col].transform(calculate_expanding_mean)
        weather[day_avg_col_name] = weather.groupby(weather.index.dayofyear)[col].transform(calculate_expanding_mean)

    weather

    predictors = weather.columns[~weather.columns.isin(["target", "name", "station","preciptype","sunrise","sunset","conditions", "description", "icon","stations"])]

    predictors

    predictions = backtest(weather, rr, predictors)
    mean_absolute_error(predictions["actual"], predictions["prediction"])

    mean_squared_error(predictions["actual"], predictions["prediction"])

    predictions.sort_values("diff", ascending=False)

    weather.loc["2021-05-01": "2021-05-10"]

    predictions["diff"].round().value_counts().sort_index()

    predictions
