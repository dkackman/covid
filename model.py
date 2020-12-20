from sklearn.linear_model import LinearRegression
from sklearn import metrics
import numpy as np
import pandas as pd
import datetime as dt


def FindBestModelOffset(new_cases, new_deaths, max_offset):
    bestModel = None
    bestR2 = 0.0
    bestPredictions = None
    bestDeaths = None
    bestOffset = 0

    # loop through the offsets for the one where cases best correlate to future deaths
    for offset in range(1, max_offset):
        cases = new_cases[-0:-offset]
        deaths = new_deaths[offset:]

        model, r2, predictions = Model(cases, deaths)
        if (r2 > bestR2):
            bestModel = model
            bestR2 = r2
            bestPredictions = predictions
            bestDeaths = deaths
            bestOffset = offset

    return bestModel, bestR2, bestPredictions, bestDeaths, bestOffset


def Model(cases, deaths):
    model = LinearRegression()
    model.fit(cases, deaths)
    predictions = model.predict(cases)
    r2 = metrics.r2_score(deaths, predictions)

    return model, r2, predictions


def Predict(model, dates, cases, deaths, offset):
    # create a new date series for the range over which we will predict
    minDate = np.amin(dates)
    maxDate = np.amax(dates) + np.timedelta64(offset + 1, 'D')

    projected_dates = pd.Series([date for date in np.arange(minDate, maxDate, dt.timedelta(days=1))])
    predicted_deaths = model.predict(cases)

    # pad deaths with enough nan values to make the same length as the projection
    empty = np.empty(offset)
    empty[:] = np.nan
    emptySeries = pd.Series(empty)

    actual_deaths = deaths.append(emptySeries)
    projected_deaths = emptySeries.append(pd.Series(predicted_deaths))

    return projected_dates, actual_deaths, projected_deaths
