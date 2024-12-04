# -*- coding: utf-8 -*-
from brownie import ContractFactory, accounts, Distributor
import json

def main():
    account = accounts[0]
    
    # Read the factory address from the JSON file
    with open("factory_address.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        factory_address = data["address"]
    
    # Access the factory contract
    factory = ContractFactory.at(factory_address)
    
    # Create a new distributor
    tx = factory.createDistributor({"from": account})
    distributor_address = tx.events["DistributorCreated"]["distributorAddress"]
    print(f"Distributor created at: {distributor_address}")
    
    # Save the distributor address to a JSON file
    with open("distributor_address.json", "w", encoding="utf-8") as f:
        json.dump({"address": distributor_address}, f)
    print("Address saved")
