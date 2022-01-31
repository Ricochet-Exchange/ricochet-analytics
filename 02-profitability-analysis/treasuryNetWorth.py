## Ricochet Bank Treasury Net Worth
## This app calculates the value of assets held in the Ricochet treasury
# to run this app local first run 'export FLASK_APP= treasuryNetWorth'
# then create a .env file with a line: polygon_url ="INSERT YOUR URL HERE"
# run with "flask run" command

from flask import Flask
from web3 import Web3
import json
import os
from dotenv import load_dotenv
from pycoingecko import CoinGeckoAPI

## IMPROVEMENTS TO BE MADE
# 1. Use loops and OOP instead of calculating each token line by line
# 2. Fix errors for bank v1 and bank v0
# 3. Add borrowed - repayed bank money to the overall calcualtion


cg = CoinGeckoAPI()

load_dotenv()


ricochet_contract_address = "0x263026E7e53DBFDce5ae55Ade22493f828922965"
daix_contract_address = "0x1305F6B6Df9Dc47159D12Eb7aC2804d4A33173c2"
wethx_contract_address = "0x27e1e4E6BC79D93032abef01025811B7E4727e85"
usdcx_contract_address = "0xCAa7349CEA390F89641fe306D93591f87595dc1F"
wbtcx_contract_address = "0x4086eBf75233e8492F1BCDa41C7f2A8288c2fB92"
mkrx_contract_address = "0x2c530aF1f088B836FA0dCa23c7Ea50E669508C4C"
maticx_contract_address = "0x3aD736904E9e65189c3000c7DD2c8AC8bB7cD4e3"
sushix_contract_address = "0xDaB943C03f9e84795DC7BF51DdC71DaF0033382b"
idlex_contract_address = "0xB63E38D21B31719e6dF314D3d2c351dF0D4a9162"

erc_contract_abi = ('[{"constant": true,"inputs": [],"name": "name","outputs": [{"name": "","type": "string"}],"payable": false,"type": "function"},{"constant": true,"inputs": [],"name": "decimals","outputs": [{"name": "","type": "uint8"}],"payable": false,"type": "function"},{"constant": true,"inputs": [{"name": "_owner","type": "address"}],"name": "balanceOf","outputs": [{"name": "balance","type": "uint256"}],"payable": false,"type": "function"},{"constant": true,"inputs": [],"name": "symbol","outputs": [{"name": "", "type": "string"}],"payable": false,"type": "function"}]')

bank_v1_1_address = "0xe78dC447d404695541b540F2FbB7682fd24d778B"
bank_v1_0_address = "0xaD39F774A75C7673eE0c8Ca2A7b88454580D7F53"
bank_v0_address = "0x91093c77720e744F415D33551C2fC3FAf7333c8c"

bank_contract_abi = ('[{"inputs":[{"internalType":"address payable","name":"oracleContract","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"borrower","type":"address"},{"indexed":false,"internalType":"uint256","name":"debtAmount","type":"uint256"}],"name":"Liquidation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"price","type":"uint256"}],"name":"PriceUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"ReserveDeposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"ReserveWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"borrower","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"VaultBorrow","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"VaultDeposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"borrower","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"VaultRepay","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"borrower","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"VaultWithdraw","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"KEEPER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REPORTER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"keeper","type":"address"}],"name":"addKeeper","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"updater","type":"address"}],"name":"addReporter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getBankFactoryOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCollateralTokenAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCollateralTokenLastUpdatedAt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCollateralTokenPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCollateralTokenPriceGranularity","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCollateralizationRatio","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_requestId","type":"uint256"}],"name":"getCurrentValue","outputs":[{"internalType":"bool","name":"ifRetrieve","type":"bool"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"_timestampRetrieved","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getDebtTokenAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getDebtTokenLastUpdatedAt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getDebtTokenPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getDebtTokenPriceGranularity","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getInterestRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getLiquidationPenalty","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getName","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOriginationFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getReserveBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getReserveCollateralBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"getRoleMember","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleMemberCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getVaultCollateralAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"vaultOwner","type":"address"}],"name":"getVaultCollateralizationRatio","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getVaultDebtAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getVaultRepayAmount","outputs":[{"internalType":"uint256","name":"principal","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"creator","type":"address"},{"internalType":"string","name":"bankName","type":"string"},{"internalType":"uint256","name":"interestRate","type":"uint256"},{"internalType":"uint256","name":"originationFee","type":"uint256"},{"internalType":"uint256","name":"collateralizationRatio","type":"uint256"},{"internalType":"uint256","name":"liquidationPenalty","type":"uint256"},{"internalType":"uint256","name":"period","type":"uint256"},{"internalType":"address","name":"bankFactoryOwner","type":"address"},{"internalType":"address payable","name":"oracleContract","type":"address"}],"name":"init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"vaultOwner","type":"address"}],"name":"liquidate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"reserveDeposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"reserveWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"reserveWithdrawCollateral","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"oldKeeper","type":"address"}],"name":"revokeKeeper","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"oldUpdater","type":"address"}],"name":"revokeReporter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"setBankFactoryOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"collateralToken","type":"address"},{"internalType":"uint256","name":"collateralTokenTellorRequestId","type":"uint256"},{"internalType":"uint256","name":"collateralTokenPriceGranularity","type":"uint256"},{"internalType":"uint256","name":"collateralTokenPrice","type":"uint256"}],"name":"setCollateral","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"debtToken","type":"address"},{"internalType":"uint256","name":"debtTokenTellorRequestId","type":"uint256"},{"internalType":"uint256","name":"debtTokenPriceGranularity","type":"uint256"},{"internalType":"uint256","name":"debtTokenPrice","type":"uint256"}],"name":"setDebt","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"updateCollateralPrice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"updateDebtPrice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"vaultBorrow","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"vaultDeposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"vaultRepay","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"vaultWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"vaults","outputs":[{"internalType":"uint256","name":"collateralAmount","type":"uint256"},{"internalType":"uint256","name":"debtAmount","type":"uint256"},{"internalType":"uint256","name":"createdAt","type":"uint256"}],"stateMutability":"view","type":"function"}]')


## Connect a node
#url = os.environ.get("polygon_url")
web3 = Web3(Web3.HTTPProvider('https://polygon-mainnet.g.alchemy.com/v2/k3hLPM5T4DGk5VBO_6-3dZzEZOHvye1L'))

## Connect to contract abi functions
Ric = web3.eth.contract(address= ricochet_contract_address, abi= erc_contract_abi)
Daix = web3.eth.contract(address= daix_contract_address, abi= erc_contract_abi)
Wethx = web3.eth.contract(address= wethx_contract_address, abi= erc_contract_abi)
Usdcx = web3.eth.contract(address= usdcx_contract_address, abi= erc_contract_abi)
Wbtcx = web3.eth.contract(address= wbtcx_contract_address, abi= erc_contract_abi)
Mkrx = web3.eth.contract(address= mkrx_contract_address, abi= erc_contract_abi)
Maticx = web3.eth.contract(address= maticx_contract_address, abi= erc_contract_abi)
Sushix = web3.eth.contract(address= sushix_contract_address, abi= erc_contract_abi)
Idlex = web3.eth.contract(address= idlex_contract_address, abi= erc_contract_abi)

# contracts = [ricochet_contract_address, daix_contract_address, wethx_contract_address, usdcx_contract_address, wbtcx_contract_address, mkrx_contract_address, maticx_contract_address, sushix_contract_address, idlex_contract_address]
#
# tokens = []
# for i in contracts:
#     tokens.append(web3.eth.contract(address= idlex_contract_address, abi= erc_contract_abi))


bank_v1_1 = web3.eth.contract(address= bank_v1_1_address, abi= bank_contract_abi)
bank_v1_0 = web3.eth.contract(address= bank_v1_0_address, abi= bank_contract_abi)
bank_v0 = web3.eth.contract(address= bank_v0_address, abi= bank_contract_abi)

bank_v1_1_borrow = bank_v1_1.events.VaultBorrow.createFilter(fromBlock='0x0')
bank_v1_0_borrow = bank_v1_0.events.VaultBorrow.createFilter(fromBlock='0x0')
print(bank_v1_0_borrow.get_all_entries())

bank_v0_borrow = bank_v0.events.VaultBorrow.createFilter(fromBlock='0x0')

bank_v1_1_repay = bank_v1_1.events.VaultRepay.createFilter(fromBlock='0x0')
bank_v1_0_repay = bank_v1_0.events.VaultRepay.createFilter(fromBlock='0x0')
bank_v0_repay = bank_v0.events.VaultRepay.createFilter(fromBlock='0x0')


#banks = [bank_v1_1_address, bank_v1_0_address, bank_v0_address]

borrowed = 0
for elem in bank_v1_1_borrow.get_all_entries():
    borrowed += elem['args']['amount']
for elem in bank_v1_0_borrow.get_all_entries():
    borrowed += elem['args']['amount']
for elem in bank_v0_borrow.get_all_entries():
    borrowed += elem['args']['amount']

repayed = 0
for elem in bank_v1_1_repay.get_all_entries():
    repayed += elem['args']['amount']
for elem in bank_v1_0_repay.get_all_entries():
    repayed += elem['args']['amount']
for elem in bank_v0_repay.get_all_entries():
    repayed += elem['args']['amount']

print(borrow*1E-18 - repay*1E-18)


ric_price = cg.get_price(ids = 'richochet', vs_currencies='usd')
daix_price = cg.get_price(ids = 'dai', vs_currencies='usd')
wethx_price = cg.get_price(ids = 'ethereum', vs_currencies='usd')
usdx_price = cg.get_price(ids = 'usd-coin', vs_currencies='usd')
btcx_price = cg.get_price(ids = 'bitcoin', vs_currencies='usd')
mkrx_price = cg.get_price(ids = 'maker', vs_currencies='usd')
maticx_price = cg.get_price(ids = 'matic-network', vs_currencies='usd')
sushix_price = cg.get_price(ids = 'sushi', vs_currencies='usd')
idlex_price = cg.get_price(ids = 'idle', vs_currencies='usd')

#print(idlex_price['idle']['usd'])

treasury_address =  "0x9C6B5FdC145912dfe6eE13A667aF3C5Eb07CbB89"


app = Flask(__name__)

@app.route("/")
def circulating_supply():
    #Find treasury balance (only one address)
    ric_balance = Ric.functions.balanceOf(treasury_address).call()*1E-18*ric_price['richochet']['usd']
    dai_balance = Daix.functions.balanceOf(treasury_address).call()*1E-18*daix_price['dai']['usd']
    eth_balance = Wethx.functions.balanceOf(treasury_address).call()*1E-18*wethx_price['ethereum']['usd']
    usd_balance = Usdcx.functions.balanceOf(treasury_address).call()*1E-18*usdx_price['usd-coin']['usd']
    btc_balance = Wbtcx.functions.balanceOf(treasury_address).call()*1E-18*btcx_price['bitcoin']['usd']
    mkr_balance = Mkrx.functions.balanceOf(treasury_address).call()*1E-18*mkrx_price['maker']['usd']
    matic_balance = Maticx.functions.balanceOf(treasury_address).call()*1E-18*maticx_price['matic-network']['usd']
    sushi_balance = Sushix.functions.balanceOf(treasury_address).call()*1E-18*sushix_price['sushi']['usd']
    idle_balance = Idlex.functions.balanceOf(treasury_address).call()*1E-18*idlex_price['idle']['usd']




     # Report Results as python dict
    return   {
       "Ric value in USD": ric_balance,
       "DAIx value in USD": dai_balance,
       "WETHx value in USD": eth_balance,
       "USDCx value in USD": usd_balance,
       "WBTCx value in USD": btc_balance,
       "MKRx value in USD": mkr_balance,
       "MATICx value in USD": matic_balance,
       "SUSHIx value in USD": sushi_balance,
       "IDLEx value in USD": idle_balance,
       "Total Treasury Value": (ric_balance + dai_balance + eth_balance + usd_balance + btc_balance + mkr_balance + matic_balance + sushi_balance + idle_balance)
       }
