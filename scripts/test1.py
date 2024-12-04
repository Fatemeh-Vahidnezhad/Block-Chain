from brownie import DrugManufacturer, Distributor, accounts
import json


def main():
    # select an account
    account = accounts[0]
    # address of manufacturer:
    with open("manufacturer_address.json", "r") as f:
        data = json.load(f)
        manufacturer_address = data["address"]

    # access to the  DrugManufacturer
    manufacturer = DrugManufacturer.at(manufacturer_address)  
    print(f"DrugManufacturer contract at: {manufacturer.address}")


    # address of manufacturer:
    with open("distributor_address.json", "r") as f:
        data1 = json.load(f)
        distributor_address = data1["address"]
    distributor = Distributor.at(distributor_address)  
    print(f"Distributor contract at: {distributor.address}")
    
    
    #create a new batch
    tx = manufacturer.createBatch("Paracetamol", 500, {"from": account})  
    print(tx.txid)
    # getting ID from BatchCreated
    batch_id = tx.events["BatchCreated"]["batchID"]

    batch_info = manufacturer.getBatch(batch_id)
    print(f"\nBatch {batch_id} Info:")
    print(f"  Product Name: {batch_info[0]}")
    print(f"  Batch Amount: {batch_info[1]}")
    print(f"  Production Date: {batch_info[2]}")
    print(f"  Status: {batch_info[3]}")
    
    #update batch status:
    new_status = "Delivered"
    tx_update = manufacturer.updateBatchStatus(batch_id, new_status, {"from": account})
    print(f"Batch status updated: {tx_update.txid}")
    
    
    #create a new distributor:
    tx_distribution = distributor.createDistribution(
        batch_id,
        manufacturer.address,
        accounts[1],  # address of reciever
        {"from": account}
    )
    distribution_id = tx_distribution.events["DistributionCreated"]["distributionID"]
    print(f"Distribution {distribution_id} created")

    # update status
    tx_status = distributor.updateStatus(
        distribution_id,
        "Delivered",
        {"from": account}
    )
    print(f"Status updated for distribution {distribution_id}: {tx_status.txid}")
