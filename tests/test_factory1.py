# -*- coding: utf-8 -*-
import pytest
from brownie import ContractFactory, PharmacyAndHospital, Distributor, accounts, DrugManufacturer
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_create_manufacturer():
    # ایجاد یک حساب برای تست
    owner = accounts[0]
    # استقرار قرارداد
    factory = ContractFactory.deploy({"from": owner})

    # تست ایجاد تولیدکننده
    tx = factory.createManufacturer({"from": owner})
    assert factory.getManufacturerCount() == 1  # بررسی تعداد تولیدکننده‌ها
    manufacturer_address = factory.getManufacturer(0)  # گرفتن آدرس تولیدکننده اول
    assert manufacturer_address is not None  # بررسی اینکه تولیدکننده ایجاد شده باشد

    event = tx.events["ManufacturerCreated"]
    assert event["owner"] == owner.address
    assert event["manufacturerAddress"] == manufacturer_address


def test_create_distributor():
    owner = accounts[0]
    factory = ContractFactory.deploy({"from": owner})

    # تست ایجاد توزیع‌کننده
    tx = factory.createDistributor({"from": owner})
    assert factory.getDistributorCount() == 1  # بررسی تعداد توزیع‌کننده‌ها
    distributor_address = factory.getDistributor(0)  # گرفتن آدرس توزیع‌کننده اول
    assert distributor_address is not None  # بررسی اینکه توزیع‌کننده ایجاد شده باشد

    event = tx.events["DistributorCreated"]
    assert event["owner"] == owner.address
    assert event["distributorAddress"] == distributor_address



def test_create_hospital_and_pharmacy():
    # حساب‌ها
    distributor_account = accounts[1]
    owner_account = accounts[0]

    # استقرار قرارداد فکتوری
    factory = ContractFactory.deploy({"from": owner_account})

    # ایجاد بیمارستان
    tx1 = factory.createHospital(distributor_account, {"from": owner_account})
    hospital_address = factory.getHospitals()[0]
    hospital = PharmacyAndHospital.at(hospital_address)

    assert len(factory.getHospitals()) == 1
    assert hospital_address == hospital.address
    print(f"Hospital created at: {hospital_address}")

    # ایجاد داروخانه
    tx2 = factory.createPharmacy(distributor_account, {"from": owner_account})
    pharmacy_address = factory.getPharmacies()[0]
    pharmacy = PharmacyAndHospital.at(pharmacy_address)

    assert len(factory.getPharmacies()) == 1
    assert pharmacy_address == pharmacy.address
    print(f"Pharmacy created at: {pharmacy_address}")

    # بررسی رخدادها
    event1 = tx1.events["HospitalCreated"]
    assert event1["hospitalAddress"] == hospital_address
    assert event1["owner"] == owner_account

    event2 = tx2.events["PharmacyCreated"]
    assert event2["pharmacyAddress"] == pharmacy_address
    assert event2["owner"] == owner_account




def test_produce_and_distribute_batch():
    manufacturer_account = accounts[0]
    distributor_account = accounts[1]
    receiver_account = accounts[2]

    # deploy the manufacturer contract
    manufacturer = DrugManufacturer.deploy({"from": manufacturer_account})
    print(f"Manufacturer deployed at: {manufacturer.address}")

    # create a batch by manufacturer
    tx1 = manufacturer.createBatch("VaccineBatch", 500, {"from": manufacturer_account})
    print(f"Batch created: Batch ID = 0, Product Name = 'VaccineBatch', Amount = 500")
    _, batch_amount, _, batch_status = manufacturer.getBatch(0)
    print(f"Batch Status: {batch_status}, Amount: {batch_amount}")

    # deploy the distributor contract
    distributor = Distributor.deploy({"from": distributor_account})
    print(f"Distributor deployed at: {distributor.address}")

    # transfer the batch
    tx2 = distributor.createDistribution(0, manufacturer.address, receiver_account, {"from": distributor_account})
    print(f"Distribution created: Distribution ID = 0, Receiver = {receiver_account}")

    # change the status to 'In Transit'
    tx3 = distributor.updateStatus(0, "In Transit", {"from": distributor_account})
    print("Distribution status updated to 'In Transit'.")

    # change the status to 'Delivered'
    tx4 = distributor.updateStatus(0, "Delivered", {"from": distributor_account})
    print("Distribution status updated to 'Delivered'.")


    #hospital or pharmacy
    account = accounts[3]
    pharmacy = PharmacyAndHospital.deploy({"from": account})
    pharmacy.address
    pharmacy.receiveProduct("Aspirin", 100, {"from": distributor})
    pharmacy.sellProduct(0, 20, {"from": account})
    product = pharmacy.inventory(0)
    print(product)

