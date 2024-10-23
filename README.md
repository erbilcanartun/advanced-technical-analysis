# Advanced Technical Indicators with Scientific Extensions

This repository provides a collection of conventional and experimental technical indicators, combining widely-used market tools with advanced scientific calculations. These indicators might offer a fresh perspective on market dynamics, incorporating concepts from complexity science, chaos theory, fractal analysis, and recurrence quantification analysis. The repository includes both static plots (Matplotlib) and interactive visualizations (Bokeh) to allow for in-depth exploration and analysis.

## Features

### Conventional Indicators

This collection includes widely-used technical indicators to analyze market trends:

- Simple Moving Average (SMA): A basic tool that smooths price data to identify trends.
- Exponential Moving Average (EMA): A variation of SMA with a greater emphasis on recent data points.
- Bollinger Bands: Plots standard deviations above and below a moving average to gauge volatility.
- Relative Strength Index (RSI): Measures the speed and change of price movements to identify overbought or oversold conditions.

### Scientific Indicators

In addition to conventional tools, this repository includes advanced metrics that apply scientific principles:

- Entropy: Quantifies uncertainty or disorder in price movements, offering insight into market unpredictability.
- Mutual Information: Measures the dependency between time-series data points to reveal hidden relationships within the price series.
- Multifractal Analysis: Identifies scaling behaviors in time-series data, uncovering patterns that emerge across different time horizons.
- Recurrence Quantification Analysis (RQA): Detects the recurrence of states in a system, helping to uncover hidden patterns or chaotic behavior in the market.
- Complexity Measures: Includes methods such as Lempel-Ziv complexity to gauge the randomness and structural complexity within time-series data.
- Lyapunov Exponent: A chaos indicator that quantifies the sensitivity of the system to initial conditions, helping to detect chaotic or stable behavior.

## Plotting

- Matplotlib (Static): Static charts offer a clear and concise way to visualize indicator values, making it easy to compare various calculations.
- Bokeh (Interactive): Interactive plots enable dynamic exploration of data, allowing users to zoom, pan, and hover over elements to obtain deeper insights into market behavior.

## Installation

Clone the repository:

```
git clone https://github.com/your-username/advanced-technical-indicators.git
````

Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Open the Jupyter notebook in the repository to access and customize the indicators.
1. Choose between static (Matplotlib) or interactive (Bokeh) charts for visualization.
1. Customize inputs such as timeframes and indicator parameters, then explore market data through the provided tools.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to suggest improvements or new features.

## License

This project is licensed under the GNU Affero General Public License (AGPL) v3 for non-commercial and academic use. For commercial use, a separate license agreement is required.

This project is available under a dual-licensing model:

### Academic and Non-Commercial Use

Licensed under GNU Affero General Public License v3.0 (AGPL-3.0)
- ✅ Free to use, modify, and distribute for academic and non-commercial purposes
- ✅ Must maintain open source nature of any modifications
- ✅ Must provide complete source code to users of any network service
- ✅ Modifications must be documented and shared
- ✅ Original copyright and license notices must be retained

### Commercial Use

A separate commercial license is required for commercial applications
- 💼 Enables use in proprietary software
- 💼 No requirement to disclose source code
- 💼 Custom support and development options
- 💼 Contact [artun@mail.com] for licensing terms

For full license details:
- See [LICENSE](LICENSE.md) for AGPL-3.0 terms
- See [COMMERCIAL LICENSE](COMMERCIAL_LICENSE.md) for commercial licensing information