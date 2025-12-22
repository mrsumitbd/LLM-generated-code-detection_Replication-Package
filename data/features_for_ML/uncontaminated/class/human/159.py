from .resources.search import search
from .resources.simple import simple
from .resources.coins import coins
from .resources.derivatives import derivatives
from .resources import key, ping, entities, token_lists, exchange_rates, asset_platforms, public_treasury
from .resources.exchanges import exchanges
from .resources.global_ import global_
from .resources.nfts import nfts
from .resources.onchain import onchain

class CoingeckoWithStreamedResponse:
    def __init__(self, client: Coingecko) -> None:
        self.asset_platforms = asset_platforms.AssetPlatformsResourceWithStreamingResponse(client.asset_platforms)
        self.coins = coins.CoinsResourceWithStreamingResponse(client.coins)
        self.derivatives = derivatives.DerivativesResourceWithStreamingResponse(client.derivatives)
        self.entities = entities.EntitiesResourceWithStreamingResponse(client.entities)
        self.exchange_rates = exchange_rates.ExchangeRatesResourceWithStreamingResponse(client.exchange_rates)
        self.exchanges = exchanges.ExchangesResourceWithStreamingResponse(client.exchanges)
        self.global_ = global_.GlobalResourceWithStreamingResponse(client.global_)
        self.key = key.KeyResourceWithStreamingResponse(client.key)
        self.nfts = nfts.NFTsResourceWithStreamingResponse(client.nfts)
        self.onchain = onchain.OnchainResourceWithStreamingResponse(client.onchain)
        self.ping = ping.PingResourceWithStreamingResponse(client.ping)
        self.public_treasury = public_treasury.PublicTreasuryResourceWithStreamingResponse(client.public_treasury)
        self.search = search.SearchResourceWithStreamingResponse(client.search)
        self.simple = simple.SimpleResourceWithStreamingResponse(client.simple)
        self.token_lists = token_lists.TokenListsResourceWithStreamingResponse(client.token_lists)