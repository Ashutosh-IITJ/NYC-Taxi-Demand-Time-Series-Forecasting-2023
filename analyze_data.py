import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.tsa.seasonal import STL
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX

def analyze():
    OUTPUT_DIR = "results"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv("aggregated_outputs/daily_trip_counts.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")

    series = df["trip_count"]


    # ===========================================================
    # 3. STL DECOMPOSITION
    # ===========================================================

    stl = STL(series, period=7)
    res = stl.fit()

    trend = res.trend
    seasonal = res.seasonal
    residual = res.resid

    plt.figure(figsize=(10, 4))
    plt.plot(trend)
    plt.title("Trend Component (STL)")
    plt.grid(True)
    plt.savefig(f"{OUTPUT_DIR}/decomposition_trend.png", dpi=300)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(seasonal)
    plt.title("Seasonal Component (STL)")
    plt.grid(True)
    plt.savefig(f"{OUTPUT_DIR}/decomposition_seasonal.png", dpi=300)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(residual)
    plt.title("Residual Component (STL)")
    plt.grid(True)
    plt.savefig(f"{OUTPUT_DIR}/decomposition_residual.png", dpi=300)
    plt.close()


    # ===========================================================
    # 4. SEASONAL STRENGTH (Hyndman & Athanasopoulos formula)
    # ===========================================================

    Fs = max(0, 1 - (np.var(residual) / np.var(residual + seasonal)))

    with open(f"{OUTPUT_DIR}/seasonal_strength.txt", "w") as f:
        f.write("Seasonal Strength (Hyndman Formula)\n")
        f.write("------------------------------------\n")
        f.write(f"F_s = {Fs:.4f}\n")

    print(f"Seasonal Strength: {Fs:.4f}")


    # ===========================================================
    # 5. AUTOCORRELATION (ACF) & PARTIAL ACF (PACF)
    # ===========================================================

    plt.figure(figsize=(10, 4))
    plot_acf(series, lags=200)
    plt.title("Autocorrelation Function (ACF)")
    plt.savefig(f"{OUTPUT_DIR}/acf_plot.png", dpi=300)
    plt.close()

    plt.figure(figsize=(10, 4))
    plot_pacf(series, lags=50, method="ywm")
    plt.title("Partial Autocorrelation Function (PACF)")
    plt.savefig(f"{OUTPUT_DIR}/pacf_plot.png", dpi=300)
    plt.close()


    # ===========================================================
    # 6. SARIMA SEASONAL MODEL (TEST SEASONAL SIGNIFICANCE)
    # ===========================================================

    model = SARIMAX(series,
                    order=(1,1,1),
                    seasonal_order=(1,1,1,7))

    result = model.fit(disp=False)

    # Save SARIMA summary
    with open(f"{OUTPUT_DIR}/sarima_summary.txt", "w") as f:
        f.write(str(result.summary()))

    # ===========================================================
    # 7. OPTIONAL: SAVE DECOMPOSITION VALUES AS CSV
    # ===========================================================

    df_out = pd.DataFrame({
        "trend": trend,
        "seasonal": seasonal,
        "residual": residual
    })

    df_out.to_csv(f"{OUTPUT_DIR}/decomposition_components.csv")

if __name__ == '__main__':
    analyze()
