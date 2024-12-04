// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DrugManufacturer {
    struct Batch {
        string productName;
        uint256 batchAmount;
        uint256 productionDate;
        string status; // Produced, Delivered, Received
    }

    mapping(uint256 => Batch) public batches;
    uint256 public nextBatchID;

    event BatchCreated(uint256 batchID, string productName, uint256 batchAmount, uint256 productionDate, string status);
    event BatchStatusUpdated(uint256 batchID, string newStatus);

    // ایجاد بچ جدید
    function createBatch(string memory productName, uint256 batchAmount) public {
        batches[nextBatchID] = Batch(productName, batchAmount, block.timestamp, "Produced");
        emit BatchCreated(nextBatchID, productName, batchAmount, block.timestamp, "Produced");
        nextBatchID++;
    }

    // به‌روزرسانی وضعیت بچ
    function updateBatchStatus(uint256 batchID, string memory newStatus) public {
        require(batchID < nextBatchID, "Batch ID does not exist");
        batches[batchID].status = newStatus;
        emit BatchStatusUpdated(batchID, newStatus);
    }

    // دریافت اطلاعات یک بچ
    function getBatch(uint256 batchID) public view returns (string memory, uint256, uint256, string memory) {
        require(batchID < nextBatchID, "Batch ID does not exist");
        Batch memory batch = batches[batchID];
        return (batch.productName, batch.batchAmount, batch.productionDate, batch.status);
    }
}
