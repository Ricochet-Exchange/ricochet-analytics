# Ricochet Analytics

## 1. Dune Analytics

Contains the queries behind the Ricochet Dune Analytics Dashboard at https://dune.xyz/mikeghen1/Ricochet-Exchange

## 2. Profitability Analysis

Python scripts which assess the profitability of Ricochet's stream markets. This involves comparing the cost of running keepers (gas) against the fees earned by these markets.

## 3. $RIC Supply and Price Endpoint

A deployed HTTPS endpoint with RIC token supply and price data. This endpoint would be utilized by token data viewing services such as CoinGecko to display.

## 4. DAO Treasury Net Worth

* Python scripts that calculates the true total net worth of Ricochet's DAO treasury.
    - TotalNetWorth = Sum(TokenBalances) + Sum(AmountOnLoanFromBank)

* Brownie framework for structure of scripts and contracts/interfaces utilized

* Alchemy websocket utilized within the brownie networks setup under id polygon-main-ws

## 5. Ricochet subgraph

Contains the [Ricochet Exchange subgraph](https://thegraph.com/hosted-service/subgraph/ricochet-exchange/ricochet-exchange) source code