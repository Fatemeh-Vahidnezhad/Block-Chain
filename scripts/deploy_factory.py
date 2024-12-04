# -*- coding: utf-8 -*-
from brownie import ContractFactory, accounts
import json

def main():
    account = accounts[0]
    
    # دیپلوی کردن فکتوری
    factory = ContractFactory.deploy({"from": account})
    print(f"Factory deployed at: {factory.address}")
    
    # ذخیره آدرس فکتوری در فایل JSON
    with open("factory_address.json", "w", encoding="utf-8") as f:
        json.dump({"address": factory.address}, f)
    print("address saved")

