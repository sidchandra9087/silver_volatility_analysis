Silver Futures Volatility Regime Strategy


This project studies whether volatility-based position sizing improves risk-adjusted performance in silver futures.
Instead of remaining fully invested at all times, the strategy adjusts exposure depending on the prevailing volatility regime. The objective is to examine whether reducing exposure during unstable periods improves capital efficiency and reduces drawdowns.

The benchmark is a simple 100 percent long exposure to silver futures.

My research question for the project:
Can a volatility adjusted model improve risk-adjusted returns in silver by dynamically adjusting position size?

The methodology:

Data
Asset: Silver Futures (SI=F)
Source: Yahoo Finance via yfinance
Frequency: Daily data
Period: 2015 to present

Step 1: Returns

Daily percentage returns are calculated from adjusted close prices.

Step 2: Volatility Regimes

A 30-day rolling standard deviation of returns is computed and annualized.

Volatility regimes are defined using percentile thresholds:

Low volatility: bottom 33 percent
Medium volatility: middle 33 percent
High volatility: top 33 percent

Step 3: Position Sizing

Exposure rules:

Low volatility → 100 percent allocation
Medium volatility → 60 percent allocation
High volatility → 30 percent allocation

This creates a volatility-prone strategy.

The benchmark remains 100 percent invested throughout.

Performance Metrics

The following metrics are computed for both strategies:

Annualized return
Annualized volatility
Sharpe ratio
Maximum drawdown
Calmar ratio
Rolling Sharpe ratios and drawdowns are also analyzed.

Key Findings

The volatility regime strategy significantly reduces maximum drawdown compared to the benchmark.
However, it also reduces overall return. In this sample, the Sharpe ratio does not improve relative to the benchmark.
This suggests that in silver, high volatility often coincides with strong upward trends. Reducing exposure during high volatility periods may limit participation in major rallies.
Volatility targeting improves capital preservation but does not necessarily enhance return efficiency in a trend-driven commodity.

Interpretation

Volatility alone may not be sufficient for optimal exposure management in silver.
Unlike broad equity indices, commodities frequently experience volatility expansion during strong directional moves. 
A pure volatility-based reduction rule can therefore sacrifice upside during explosive rallies.

A potential extension of this project could combine volatility and momentum signals to differentiate between destabilizing volatility and trend-driven volatility.

The limitations of this model:

Volatility is measured using a fixed 30-day window.
No transaction costs are included.
Regime thresholds are static.
The model does not incorporate momentum or macro variables.
Futures roll effects are not explicitly modeled.

The conclusion:

This project demonstrates the trade-off between drawdown control and return maximization in commodities.
Volatility targeting reduces downside risk but may underperform during sustained high-volatility rallies.
The results highlight the importance of regime awareness and the limits of single-factor risk models in commodity markets.