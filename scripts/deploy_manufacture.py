# -*- coding: utf-8 -*-
from brownie import ContractFactory, accounts, DrugManufacturer
import json

def main():
    account = accounts[0]
    
    # آدرس فکتوری را از فایل JSON بخوانید
    with open("factory_address.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        factory_address = data["address"]
    
    # دسترسی به قرارداد فکتوری
    factory = ContractFactory.at(factory_address)
    
    # ایجاد یک تولیدکننده جدید
    tx = factory.createManufacturer({"from": account})
    manufacturer_address = tx.events["ManufacturerCreated"]["manufacturerAddress"]
    print(f"Manufacturer created at: {manufacturer_address}")
    
    # ذخیره آدرس تولیدکننده در فایل JSON
    with open("manufacturer_addresses.json", "w", encoding="utf-8") as f:
        json.dump({"address": manufacturer_address}, f)
    print("address saved")
