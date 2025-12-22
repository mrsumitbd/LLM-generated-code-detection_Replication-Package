class MarketChartResourceWithStreamingResponse:

    def __init__(self, market_chart: MarketChartResource) -> None:
        self.market_chart = market_chart

    def get_data(self):
        # Implement the logic to get streaming response data from market_chart
        pass

    def process_data(self, data):
        # Implement the logic to process the streaming response data
        pass

    def display_chart(self):
        # Implement the logic to display the chart using the processed data
        pass

# Sample usage
market_chart = MarketChartResource()
market_chart_with_streaming_response = MarketChartResourceWithStreamingResponse(market_chart)
market_chart_with_streaming_response.get_data()
market_chart_with_streaming_response.process_data(data)
market_chart_with_streaming_response.display_chart()