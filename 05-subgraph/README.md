# Ricochet Subgraph

Official subgraph for the Ricochet Exchange smart contracts

### Local development

0. Ensure you have `yarn`, `docker` and `docker-compose` installed

1. Install dependencies by running `yarn`

2. Start graph-node locally in docker by running `RPC_URL={rpc_endpoint} docker-compose up`, where `{rpc_endpoint}` is a Matic RPC endpoint, e.g from [Alchemy](https://alchemy.com)

3. Bind contracts to specific addresses in the mappings by running  `graph codegen`

4. Run `yarn create-local && yarn deploy-local` to build and deploy the subgraph locally

5. Visit `http://localhost:8000/subgraphs/name/ricochet-exchange/ricochet-exchange/graphql` to query the subgraph using GraphQL

6. Stop the `docker-compose` service when done

### Deploying the subgraph

* See instructions [here](https://thegraph.com/docs/en/hosted-service/deploy-subgraph-hosted/)

* Should be deployed using Ricochet Exchange GitHub organization's access token
