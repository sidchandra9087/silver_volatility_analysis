import numpy as np


def cumulative_returns(returns):
    return (1 + returns).cumprod()


def annualized_return(returns):
    n = len(returns)
    total = (1 + returns).prod()
    return total ** (252 / n) - 1


def annualized_vol(returns):
    return returns.std() * np.sqrt(252)


def sharpe_ratio(returns, rf=0.0):
    excess = returns - rf / 252
    return (excess.mean() / excess.std()) * np.sqrt(252)


def max_drawdown(returns):
    cum = (1 + returns).cumprod()
    peak = cum.cummax()
    dd = (cum - peak) / peak
    return dd.min()


def calmar_ratio(returns):
    ann_ret = annualized_return(returns)
    mdd = abs(max_drawdown(returns))
    if mdd == 0:
        return float("nan")
    return ann_ret / mdd


def drawdown_series(returns):
    cum = (1 + returns).cumprod()
    peak = cum.cummax()
    return (cum - peak) / peak


def rolling_sharpe(returns, window=60):
    def sharpe_window(r):
        if r.std() == 0:
            return float("nan")
        return (r.mean() / r.std()) * np.sqrt(252)
    return returns.rolling(window).apply(sharpe_window, raw=True)


def comparison_table(strat_returns, bench_returns):
    metrics = {
        "Annualized Return": (annualized_return(strat_returns), annualized_return(bench_returns)),
        "Annualized Vol":    (annualized_vol(strat_returns),    annualized_vol(bench_returns)),
        "Sharpe Ratio":      (sharpe_ratio(strat_returns),      sharpe_ratio(bench_returns)),
        "Max Drawdown":      (max_drawdown(strat_returns),      max_drawdown(bench_returns)),
        "Calmar Ratio":      (calmar_ratio(strat_returns),      calmar_ratio(bench_returns)),
    }

    pct_keys = {"Annualized Return", "Annualized Vol", "Max Drawdown"}

    print(f"\n{'Metric':<22} {'Dynamic Strategy':>18} {'Benchmark':>18}")
    print("-" * 60)
    for k, (s, b) in metrics.items():
        if k in pct_keys:
            print(f"{k:<22} {s:>17.2%} {b:>17.2%}")
        else:
            print(f"{k:<22} {s:>18.2f} {b:>18.2f}")


def summarize(returns, label):
    print(f"\n--- {label} ---")
    print(f"Annualized Return : {annualized_return(returns):.2%}")
    print(f"Annualized Vol    : {annualized_vol(returns):.2%}")
    print(f"Sharpe Ratio      : {sharpe_ratio(returns):.2f}")
    print(f"Max Drawdown      : {max_drawdown(returns):.2%}")