# Example of creating Tool in the Agentic Framework
Created class StockAnalysisTool. It contains three functions:

`raw_data = self.fetch_stock_data(symbol, start_date, end_date)`

`analyzed_data = self.calculate_indicators(raw_data)`

`self.plot_stock_data_interactive(analyzed_data, symbol)`

## Enhancements Pending
Need to check if LLM is being called. Do not want it to be called.

I also want to pass arguments into the tool, and not have LLM do it. 