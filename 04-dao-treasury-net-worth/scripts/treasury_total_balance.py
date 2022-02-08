from brownie import web3, Contract, SuperToken, Bank, BankOld
from pycoingecko import CoinGeckoAPI
from time import sleep
from scripts.constants import TOKENS, BANKS, TREASURY_ADDRESS, BANK_BLOCK_START

cg = CoinGeckoAPI()

def get_price(token):
    return cg.get_price(ids=token, vs_currencies='usd')

def get_contract(symbol, address, abi, is_token):
    if(is_token):
        return Contract.from_abi(symbol, address, abi)
    else:
        return web3.eth.contract(address=address, abi=abi)

def calculate_token_total():
    total_token_value_usd = 0

    for token_symbol, token_address in TOKENS.items():
        token = get_contract(token_symbol, token_address, SuperToken.abi, True)
        balance = web3.fromWei(token.balanceOf(TREASURY_ADDRESS), 'ether')
        balance_in_usd = float(balance) * get_price(token_symbol)[token_symbol]['usd']
        print(f"Treasury currently has a USD balance of {balance_in_usd} in {token_symbol}")
        total_token_value_usd += balance_in_usd
    print(f"Total Token Value in USD: {total_token_value_usd}")
    return total_token_value_usd
        

def calculate_bank_loans():
    total_borrowed = 0
    event_signature_hash = web3.sha3(text="VaultBorrow(address,uint256)").hex()
    for bank_name, bank_address in BANKS.items():
        start =  BANK_BLOCK_START[bank_name]
        batch_size = 100
        total_end = web3.eth.get_block_number()
        print(f"Current Bank: {bank_name}")
        print(f"Current Event: VaultBorrow")
        if bank_name == 'v1.1':
            bank = get_contract(bank_name, bank_address, Bank.abi, False)
        else:
            bank = get_contract(bank_name, bank_address, BankOld.abi, False)
        for i in range(start, total_end, batch_size):
            event_filter = bank.events.VaultBorrow.createFilter(fromBlock=i, toBlock=i+batch_size, topics=[None])
            for event in event_filter.get_all_entries():
                total_borrowed += web3.fromWei(int(event['args']['amount']), 'ether')
                print(event)
        sleep(3)

    total_repayed = 0
    event_signature_hash = web3.sha3(text="VaultRepay(address,uint256)").hex()
    for bank_name, bank_address in BANKS.items():
        start =  BANK_BLOCK_START[bank_name]
        batch_size = 100
        total_end = web3.eth.get_block_number()
        if bank_name == 'v1.1':
            bank = get_contract(bank_name, bank_address, Bank.abi, False)
        else:
            bank = get_contract(bank_name, bank_address, BankOld.abi, False)
        print(f"Current Bank: {bank_name}")
        print(f"Current Event: VaultRepay")
        for i in range(start, total_end, batch_size):
            event_filter = bank.events.VaultRepay.createFilter(fromBlock=i, toBlock=i+batch_size, topics=event_signature_hash)
            for event in event_filter.get_all_entries():
                total_repayed += web3.fromWei(int(event['args']['amount']), 'ether')
        sleep(3)

    total_USDC = 0
    usdc = get_contract('usdc', TOKENS['usd-coin'], SuperToken.abi, True)
    print(f"Calculating USDC Total...")
    for bank_name, bank_address in BANKS.items():
        total_USDC += web3.fromWei(usdc.balanceOf(bank_address), 'ether')
        print(f"Current Bank: {bank_name}")

    print("Summing Amounts")

    return total_borrowed - total_repayed + float(total_USDC)

def calculate_total_treasury_net_worth(token_total, bank_loans):
    return token_total + bank_loans

def main():
    total_net_worth_dao_treasury = calculate_total_treasury_net_worth(calculate_token_total(), calculate_bank_loans())

    print(f"Total Net Worth for Ricochet DAO Tresury {total_net_worth_dao_treasury}")

if __name__ == '__main__':
    main()