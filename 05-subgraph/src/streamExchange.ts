import { Address, BigInt, log } from "@graphprotocol/graph-ts"
import {
  StreamExchange,
  UpdatedStream,
  Distribution
} from "../generated/StreamExchange/StreamExchange"
import { DistributionEvent, UpdatedStreamEvent, Keeper, Market, Streamer, Stream } from "../generated/schema"

export function handleUpdatedStream(event: UpdatedStream): void {
  updateMarket(event.address)
  const stream = updateStream(event)
  const updatedStream = new UpdatedStreamEvent(`${event.transaction.hash.toHex()}-${event.logIndex.toString()}`)
  updatedStream.blockNumber = event.block.number
  updatedStream.timestamp = event.block.timestamp
  updatedStream.transactionHash = event.transaction.hash
  updatedStream.from = event.params.from
  updatedStream.stream = stream
  updatedStream.newFlowRate = event.params.newRate
  updatedStream.newTotalFlowRate = event.params.totalInflow
  updatedStream.save()
}

export function handleDistribution(event: Distribution): void {
  const market = updateMarket(event.address)
  const distribution = new DistributionEvent(`${event.transaction.hash.toHex()}-${event.logIndex.toString()}`)
  // Only set keeper if event originates from external distribute() function call
  if (event.transaction.input.toHex().startsWith("0xe4fc6b6d")) {
    const keeper = updateKeeper(event.transaction.from)
    distribution.keeper = keeper
  }
  distribution.blockNumber = event.block.number
  distribution.timestamp = event.block.timestamp
  distribution.transactionHash = event.transaction.hash
  distribution.from = event.transaction.from
  distribution.market = market
  distribution.distributedAmount = event.params.totalAmount
  distribution.collectedFeeAmount = event.params.feeCollected
  distribution.token = event.params.token
  distribution.save()
}

function updateStream(event: UpdatedStream): string {
  const streamer = updateStreamer(event.params.from)
  let stream = Stream.load(`${event.address.toHex()}-${event.params.from.toHex()}`)
  if (!stream) {
    stream = new Stream(`${event.address.toHex()}-${event.params.from.toHex()}`)
    stream.market = event.address.toHex()
    stream.updatedAt = event.block.timestamp
    stream.streamer = streamer
  }
  const timeSinceLastUpdate = event.block.timestamp.minus(stream.updatedAt)
  stream.totalStreamed = stream.totalStreamed.plus(timeSinceLastUpdate.times(stream.flowRate))
  stream.flowRate = event.params.newRate
  stream.updatedAt = event.block.timestamp
  stream.save()
  return stream.id
}

function updateMarket(address: Address): string {
  let market = Market.load(address.toHex())
  if (!market) {
    const exchange = StreamExchange.bind(address)
    const inputToken = exchange.try_getInputToken()
    if (inputToken.reverted) {
      log.error("Failed to get input token for contract {}", [address.toHex()])
    }
    let outputToken = exchange.try_getOutputToken()
    if (outputToken.reverted) {
      outputToken = exchange.try_getOuputToken()
    }
    if (outputToken.reverted) {
      log.error("Failed to get output token for contract {}", [address.toHex()])
    }
    market = new Market(address.toHex())
    market.inToken = !inputToken.reverted ? inputToken.value : Address.zero()
    market.outToken = !outputToken.reverted ? outputToken.value : Address.zero()
    market.save()
  }
  return market.id
}

function updateKeeper(address: Address): string {
  let keeper = Keeper.load(address.toHex())
  if (!keeper) {
     keeper = new Keeper(address.toHex())
  }
  keeper.totalDistributions = keeper.totalDistributions + 1
  keeper.save()
  return keeper.id
}

function updateStreamer(address: Address): string {
  const streamer = new Streamer(address.toHex())
  streamer.save()
  return streamer.id
}



