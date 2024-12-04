from brownie import DrugManufacturer, accounts
import json


def main():
    account = accounts[0]
    contract = DrugManufacturer.deploy({"from": account})
    print(f"Contract deployed at: {contract.address}")
    
    #saving the address in a file
    with open("manufacturer_address.json", "w") as f:
        json.dump({"address": contract.address}, f)
