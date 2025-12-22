class MarketChartResourceWithStreamingResponse:

    def __init__(self, market_chart: MarketChartResource) -> None:
        self.market_chart = market_chart

    def get_data(self):
        # Implement logic to get streaming response data
        pass

    def process_data(self, data):
        # Implement logic to process streaming response data
        pass

    def display_chart(self):
        # Implement logic to display the chart based on processed data
        pass

# Sample usage
market_chart = MarketChartResource()
market_chart_with_streaming_response = MarketChartResourceWithStreamingResponse(market_chart)
market_chart_with_streaming_response.get_data()
processed_data = market_chart_with_streaming_response.process_data(data)
market_chart_with_streaming_response.display_chart()