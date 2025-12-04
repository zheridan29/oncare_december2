# DEFINITION OF TERMS

This section defines the key technical terms and concepts used throughout this study, explaining how each term applies to the Medicine Ordering System and making these concepts accessible to readers who may not be familiar with advanced analytics or time series forecasting.

## A

**AIC (Akaike Information Criterion)**
AIC is a statistical measure that balances model accuracy against complexity to select the best forecasting model. In the Medicine Ordering System, Auto ARIMA uses AIC to evaluate different parameter combinations when building ARIMA models for medicine demand forecasting. The system automatically selects the model with the lowest AIC score, ensuring optimal balance between prediction accuracy and model simplicity. This prevents overfitting and ensures reliable forecasts for inventory management decisions.

**ARIMA (Autoregressive Integrated Moving Average)**
ARIMA is a statistical forecasting model that analyzes time series data to predict future values based on historical patterns. In the Medicine Ordering System, ARIMA models are applied to historical sales data to forecast future demand for medicines. The model's three components—autoregressive (AR), integrated (I), and moving average (MA)—work together to capture patterns, trends, and random fluctuations in medicine sales. These forecasts help pharmacists maintain optimal inventory levels, preventing stockouts while avoiding excess inventory that may expire.

**Auto ARIMA**
Auto ARIMA is an automated feature that eliminates the need for manual parameter selection when building ARIMA forecasting models. In the Medicine Ordering System, when pharmacists request demand forecasts, Auto ARIMA systematically tests various parameter combinations and selects the optimal configuration using statistical criteria like AIC and BIC. This automation allows users to generate accurate forecasts without requiring deep statistical knowledge, as the system handles all technical model selection behind the scenes.

## B

**BIC (Bayesian Information Criterion)**
BIC is a model selection criterion similar to AIC but with a stronger penalty for model complexity, favoring simpler models. In the Medicine Ordering System, both AIC and BIC are calculated when Auto ARIMA evaluates potential ARIMA models for demand forecasting. While AIC might select a more complex model, BIC ensures the chosen model remains simple and generalizable to future predictions. This dual-criterion approach provides robust model selection, giving pharmacists confidence in forecast reliability.

## D

**Differencing**
Differencing is a data transformation technique that converts non-stationary time series data into stationary form by calculating differences between consecutive time periods. In the Medicine Ordering System, when sales data exhibits trends, the system automatically applies differencing before ARIMA modeling to remove these trends. This transformation makes the data suitable for accurate forecasting by stabilizing the statistical properties of the time series. The differencing process ensures that demand forecasts are based on stable, reliable patterns rather than temporary trends.

**Demand Forecast**
A demand forecast is a prediction of future product demand based on analysis of historical sales patterns and trends. In the Medicine Ordering System, demand forecasts tell pharmacists and inventory managers how many units of each medicine to expect in upcoming periods. These forecasts are generated using ARIMA models that examine past sales data, identify seasonal patterns (such as increased flu medication demand during winter), and project future needs. Accurate demand forecasts help pharmacies maintain optimal inventory levels—sufficient to meet patient needs without excessive capital tied up in stock that may expire.

## F

**Forecast Horizon**
Forecast horizon refers to the timeframe into the future for which predictions are made. In the Medicine Ordering System, users can specify forecast horizons ranging from weeks to months or even a full year when generating demand forecasts. Shorter horizons (one to three months) typically provide more accurate predictions due to less uncertainty, while longer horizons offer strategic planning insights with reduced precision. The system's flexibility in forecast horizon selection allows pharmacists to adjust predictions based on their specific inventory planning needs, whether for immediate restocking or annual budget planning.

## M

**MAPE (Mean Absolute Percentage Error)**
MAPE measures forecast accuracy as a percentage, indicating the average deviation of predictions from actual values. In the Medicine Ordering System, MAPE is calculated and displayed alongside demand forecasts to help pharmacists understand forecast reliability. A lower MAPE indicates more trustworthy forecasts, enabling confident inventory decision-making. The system calculates MAPE after generating forecasts, providing users with a clear metric to assess how much confidence to place in predictions.

**MAE (Mean Absolute Error)**
MAE measures forecast accuracy in absolute terms, showing the average difference between predicted and actual values in the same units as the data (e.g., number of medicine units). In the Medicine Ordering System, MAE provides practical interpretation of forecast accuracy—for example, indicating that predictions are typically off by 3 boxes of a particular medicine. Unlike percentage-based metrics, MAE gives pharmacists a tangible understanding of forecast errors in real-world terms. This helps determine appropriate buffer stock levels to account for forecast uncertainty.

## P

**Predictive Analytics**
Predictive analytics encompasses techniques and methods that use historical data, statistical algorithms, and machine learning to identify patterns and predict future events. In the Medicine Ordering System, predictive analytics powers the demand forecasting capabilities by analyzing historical sales data, detecting seasonal patterns, and generating future demand predictions. Beyond forecasting, the system uses predictive analytics to identify trends, detect anomalies (such as sudden demand spikes), and optimize inventory levels. This transforms the system from a record-keeping tool into an intelligent decision-support system that enables data-driven inventory management.

**pmdarima**
pmdarima is a Python library that simplifies ARIMA model implementation and provides automated model selection capabilities. In the Medicine Ordering System, pmdarima provides the Auto ARIMA functionality that automatically finds optimal forecasting models for each medicine's sales data. Without this library, building accurate ARIMA forecasts would require extensive statistical knowledge and manual parameter testing. The library handles complex mathematical computations, making advanced forecasting capabilities accessible to users without specialized time series analysis training.

## R

**RMSE (Root Mean Squared Error)**
RMSE measures forecast accuracy by penalizing larger errors more heavily than smaller ones, providing insight into the typical magnitude of prediction errors. In the Medicine Ordering System, RMSE is calculated alongside MAE and MAPE to provide a comprehensive picture of forecast quality. Higher RMSE values indicate less accurate predictions, helping pharmacists identify whether occasional large errors might cause inventory problems. This metric, combined with other accuracy measures, enables informed decisions about forecast reliability and appropriate safety stock levels.

## S

**Seasonal Decomposition**
Seasonal decomposition is a technique that separates time series data into its fundamental components: trend, seasonal patterns, and random fluctuations. In the Medicine Ordering System, this process helps identify strong seasonal patterns in medicine sales, such as allergy medications peaking in spring or flu vaccines spiking in fall. By understanding these components individually, the system can better account for predictable seasonal variations when generating forecasts. This improves forecast accuracy by incorporating seasonal patterns that might otherwise be overlooked.

**Stationarity**
Stationarity describes whether a time series maintains consistent statistical properties (constant mean, variance, and no trends) over time. In the Medicine Ordering System, stationarity is tested before building ARIMA models because these models work best with stationary data. If sales data shows trends or seasonality, the system automatically applies transformations like differencing to achieve stationarity. This ensures that demand forecasts are based on stable, reliable patterns rather than temporary fluctuations or trends.

## T

**Time Series**
A time series is a collection of data points recorded at regular time intervals, such as daily sales figures or monthly inventory levels. In the Medicine Ordering System, time series data includes historical medicine sales, inventory levels, and order quantities collected over weeks, months, or years. This historical data forms the foundation for demand forecasting, as the system analyzes past patterns to project future needs. When pharmacists view analytics dashboards, they're examining time series visualizations that show how medicine sales have fluctuated over time, enabling data-driven inventory planning decisions.

---

**Note on Usage in the System:**
These terms work together to create a comprehensive forecasting system. When a pharmacist requests a demand forecast for a medicine, the system first prepares time series data from historical sales. It then tests for stationarity and performs seasonal decomposition to understand the underlying patterns. Using pmdarima's Auto ARIMA functionality, the system automatically selects the best ARIMA model for that specific medicine's sales patterns. The forecast is generated and evaluated using metrics like RMSE, MAE, and MAPE to ensure accuracy. This entire process falls under the umbrella of predictive analytics—using past data to predict future needs, ultimately helping maintain optimal inventory levels and ensuring patient care isn't interrupted by stockouts.
