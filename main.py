import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec

from silver_data import fetch_silver_data
from silver_strategy import add_rolling_vol, assign_regimes, assign_exposure, compute_returns
from silver_metrics import (
    cumulative_returns, summarize, comparison_table,
    drawdown_series, rolling_sharpe,
    annualized_return, annualized_vol, sharpe_ratio, max_drawdown, calmar_ratio
)


df = fetch_silver_data()
df = add_rolling_vol(df)
df = assign_regimes(df)
df = assign_exposure(df)
df = compute_returns(df)

summarize(df["strategy_returns"], "Dynamic Strategy")
summarize(df["benchmark_returns"], "Benchmark (Buy & Hold)")

comparison_table(df["strategy_returns"], df["benchmark_returns"])

strat_cum = cumulative_returns(df["strategy_returns"])
bench_cum = cumulative_returns(df["benchmark_returns"])
strat_dd = drawdown_series(df["strategy_returns"])
bench_dd = drawdown_series(df["benchmark_returns"])
strat_rs = rolling_sharpe(df["strategy_returns"], window=60)
bench_rs = rolling_sharpe(df["benchmark_returns"], window=60)

fig = plt.figure(figsize=(16, 12))
fig.suptitle("Silver Futures — Volatility Regime Strategy Dashboard", fontsize=14, y=0.98)

gs = GridSpec(3, 2, figure=fig, height_ratios=[1.2, 1, 1], hspace=0.45, wspace=0.3)

ax1 = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[1, 1])
ax4 = fig.add_subplot(gs[2, 0])
ax5 = fig.add_subplot(gs[2, 1])

fmt = mdates.DateFormatter("%Y")

ax1.plot(strat_cum.index, strat_cum.values, label="Dynamic Strategy", color="steelblue")
ax1.plot(bench_cum.index, bench_cum.values, label="Benchmark", color="gray", alpha=0.7)
ax1.set_title("Cumulative Returns", fontsize=11)
ax1.set_ylabel("Growth of $1")
ax1.legend(fontsize=9)
ax1.xaxis.set_major_formatter(fmt)
ax1.grid(alpha=0.3)

regime_colors = {"low": "green", "medium": "orange", "high": "red"}
for regime, color in regime_colors.items():
    mask = df["regime"] == regime
    ax2.scatter(df.index[mask], df.loc[mask, "rolling_vol"], s=2, color=color, label=regime)
ax2.set_title("30-Day Rolling Volatility", fontsize=11)
ax2.set_ylabel("Annualized Vol")
ax2.legend(fontsize=8, markerscale=4)
ax2.xaxis.set_major_formatter(fmt)
ax2.grid(alpha=0.3)

ax3.fill_between(strat_dd.index, strat_dd.values, 0, alpha=0.4, color="steelblue", label="Dynamic Strategy")
ax3.fill_between(bench_dd.index, bench_dd.values, 0, alpha=0.3, color="gray", label="Benchmark")
ax3.set_title("Drawdowns", fontsize=11)
ax3.set_ylabel("Drawdown")
ax3.legend(fontsize=8)
ax3.xaxis.set_major_formatter(fmt)
ax3.grid(alpha=0.3)

ax4.plot(strat_rs.index, strat_rs.values, label="Dynamic Strategy", color="steelblue")
ax4.plot(bench_rs.index, bench_rs.values, label="Benchmark", color="gray", alpha=0.7)
ax4.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax4.set_title("Rolling 60-Day Sharpe Ratio", fontsize=11)
ax4.set_ylabel("Sharpe Ratio")
ax4.legend(fontsize=8)
ax4.xaxis.set_major_formatter(fmt)
ax4.grid(alpha=0.3)

ax5.axis("off")

metrics = [
    ("Annualized Return", annualized_return(df["strategy_returns"]), annualized_return(df["benchmark_returns"]), True),
    ("Annualized Vol",    annualized_vol(df["strategy_returns"]),    annualized_vol(df["benchmark_returns"]),    True),
    ("Sharpe Ratio",      sharpe_ratio(df["strategy_returns"]),      sharpe_ratio(df["benchmark_returns"]),      False),
    ("Max Drawdown",      max_drawdown(df["strategy_returns"]),      max_drawdown(df["benchmark_returns"]),      True),
    ("Calmar Ratio",      calmar_ratio(df["strategy_returns"]),      calmar_ratio(df["benchmark_returns"]),      False),
]

col_labels = ["Metric", "Dynamic", "Benchmark"]
table_data = []
for name, s, b, is_pct in metrics:
    if is_pct:
        table_data.append([name, f"{s:.2%}", f"{b:.2%}"])
    else:
        table_data.append([name, f"{s:.2f}", f"{b:.2f}"])

table = ax5.table(
    cellText=table_data,
    colLabels=col_labels,
    cellLoc="center",
    loc="center",
    bbox=[0.05, 0.1, 0.9, 0.85]
)
table.auto_set_font_size(False)
table.set_fontsize(9)

for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor("#cccccc")
    if row == 0:
        cell.set_facecolor("#2c3e50")
        cell.set_text_props(color="white", fontweight="bold")
    elif row % 2 == 0:
        cell.set_facecolor("#f2f2f2")
    else:
        cell.set_facecolor("white")

ax5.set_title("Performance Metrics", fontsize=11, pad=10)

plt.show()