
# **Smart Contract Testing with Brownie and Ganache**

This guide provides step-by-step instructions to install, run, and test smart contracts using Brownie and Ganache.

---

## **1. Installation**

Follow these steps to set up the required tools:

1. Install Brownie:
   ```bash
   pip install eth-brownie
   ```

2. Download and install [Node.js](https://nodejs.org/). Ensure `npm` is included during installation.

3. Install Ganache globally using `npm`:
   ```bash
   npm install -g ganache
   ```

---

## **2. Run Ganache**

Start Ganache with the following command to initialize a local Ethereum blockchain:
```bash
ganache --hardfork istanbul --miner.blockGasLimit 12000000
```

This command sets the hardfork to "Istanbul" and increases the block gas limit to `12,000,000`.

---

## **3. Compile Smart Contracts**

In a separate terminal, run the following commands:

1. Set your terminal to use UTF-8 encoding (necessary for Windows users):
   ```bash
   chcp 65001
   ```

2. Compile the smart contracts:
   ```bash
   brownie compile
   ```

---

## **4. Test Smart Contracts in Brownie Console**

Launch the Brownie console to interact with your smart contracts:
```bash
brownie console
```

---

## **5. Deploy and Test Smart Contracts**

Use the following script to deploy and test your smart contracts inside the Brownie console.

### **Step 1: Set up Accounts**
```python
manufacturer_account = accounts[0]
distributor_account = accounts[1]
receiver_account = accounts[2]
```

---

### **Step 2: Deploy and Test Manufacturer Contract**
1. **Deploy Manufacturer Contract:**
   ```python
   manufacturer = DrugManufacturer.deploy({"from": manufacturer_account})
   print(f"Manufacturer deployed at: {manufacturer.address}")
   ```

2. **Create a Batch:**
   ```python
   tx1 = manufacturer.createBatch("VaccineBatch", 500, {"from": manufacturer_account})
   print("Batch created: Batch ID = 0, Product Name = 'VaccineBatch', Amount = 500")
   _, batch_amount, _, batch_status = manufacturer.getBatch(0)
   print(f"Batch Status: {batch_status}, Amount: {batch_amount}")
   ```

---

### **Step 3: Deploy and Test Distributor Contract**
1. **Deploy Distributor Contract:**
   ```python
   distributor = Distributor.deploy({"from": distributor_account})
   print(f"Distributor deployed at: {distributor.address}")
   ```

2. **Create Distribution:**
   ```python
   tx2 = distributor.createDistribution(0, manufacturer.address, receiver_account, {"from": distributor_account})
   print(f"Distribution created: Distribution ID = 0, Receiver = {receiver_account}")
   ```

3. **Update Distribution Status:**
   - **In Transit:**
     ```python
     tx3 = distributor.updateStatus(0, "In Transit", {"from": distributor_account})
     print("Distribution status updated to 'In Transit'.")
     ```
   - **Delivered:**
     ```python
     tx4 = distributor.updateStatus(0, "Delivered", {"from": distributor_account})
     print("Distribution status updated to 'Delivered'.")
     ```

---

### **Step 4: Test Pharmacy or Hospital Contract**
1. **Deploy Pharmacy Contract:**
   ```python
   account = accounts[3]
   pharmacy = PharmacyAndHospital.deploy({"from": account})
   print(f"Pharmacy deployed at: {pharmacy.address}")
   ```

2. **Receive a Product:**
   ```python
   pharmacy.receiveProduct("Aspirin", 100, {"from": distributor})
   ```

3. **Sell a Product:**
   ```python
   pharmacy.sellProduct(0, 20, {"from": account})
   ```

4. **Check Inventory:**
   ```python
   product = pharmacy.inventory(0)
   print(product)
   ```

---

## **6. Notes**
- Ensure Ganache is running on `http://127.0.0.1:8545`.
- Use unique accounts for each role (e.g., manufacturer, distributor, receiver).
- Modify the smart contract functions as necessary for additional use cases.

---

