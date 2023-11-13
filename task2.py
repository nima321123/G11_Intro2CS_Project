import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error

class Task2:
    def analyze_weather(self, file_path):
        # Load data
        weather = pd.read_csv(file_path, index_col="datetime")

        # Display unique values in each column
        for col in weather.columns:
            unique_values = weather[col].unique()
            print(f"Column {col}: {unique_values}")

        # Handle non-numeric values
        weather.replace("your_non_numeric_value", pd.NA, inplace=True)
        weather = weather.apply(pd.to_numeric, errors='coerce')
        weather = weather.ffill().fillna(0)

        # Continue with your existing logic
        null_pct = weather.apply(pd.isnull).sum() / weather.shape[0]
        valid_columns = weather.columns[null_pct < 0.03]

        print("Valid Columns:")
        print(valid_columns)

        # Count occurrences of 9999 in each column
        occurrences_9999 = weather.apply(lambda x: (x == 9999).sum())
        print("Occurrences of 9999 in each column:")
        print(occurrences_9999)

        # Data types of each column
        data_types = weather.dtypes
        print("Data Types:")
        print(data_types)

        # Display the index
        index_values = weather.index
        print("Index Values:")
        print(index_values)

        # Convert the index to datetime
        weather.index = pd.to_datetime(weather.index)

        # Display the count of years in the index
        year_counts = weather.index.year.value_counts().sort_index()
        print("Year Counts:")
        print(year_counts)

        # Plot the 'tempmax' column
        weather["tempmax"].plot(title="Temperature Max")

        # Create the 'target' column by shifting 'tempmax'
        weather["target"] = weather["tempmax"].shift(-1)

        # Display the modified DataFrame
        print("Modified DataFrame:")
        print(weather)

        # Forward fill missing values
        weather = weather.ffill()
        print("DataFrame after Forward Fill:")
        print(weather)

        # Calculate correlation matrix
        correlation_matrix = weather.corr()
        print("Correlation Matrix:")
        print(correlation_matrix)

        # ... (continue with the rest of your code)


        rr = Ridge(alpha=0.1)

        predictors = weather.columns[~weather.columns.isin(["target", "name", "station", "preciptype", "sunrise", "sunset", "conditions", "description", "icon", "stations"])]

        def backtest(weather, model, predictors, start=30, step=10):
            all_predictions = []

            for i in range(start, weather.shape[0], step):
                train = weather.iloc[:i, :]
                test = weather.iloc[i:(i+step), :]

                model.fit(train[predictors], train["target"])

                preds = model.predict(test[predictors])
                preds = pd.Series(preds, index=test.index)
                combined = pd.concat([test["target"], preds], axis=1)
                combined.columns = ["actual", "prediction"]
                combined["diff"] = (combined["prediction"] - combined["actual"]).abs()

                all_predictions.append(combined)
            return pd.concat(all_predictions)

        weather = weather.fillna(0)

        predictions = backtest(weather, rr, predictors)
   # Print or return any relevant results
        print("Predictions:")
        print(predictions)

        # Evaluate model performance
        mae = mean_absolute_error(predictions["actual"], predictions["prediction"])
        mse = mean_squared_error(predictions["actual"], predictions["prediction"])
        print("Mean Absolute Error:", mae)
        print("Mean Squared Error:", mse)

        # Display additional results as needed
        print("Top 5 predictions with the largest differences:")
        print(predictions.sort_values("diff", ascending=False).head())

        # Subset of data for May 2021
        print("Subset of data for May 2021:")
        print(weather.loc["2021-05-01": "2021-05-10"])

        # Distribution of rounded differences in predictions
        print("Distribution of rounded differences in predictions:")
        print(predictions["diff"].round().value_counts().sort_index())
