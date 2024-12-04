// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./DrugManufacturer.sol";

contract Distributor {
    struct Distribution {
        uint256 batchID;        // ID بچ
        address manufacturer;   // آدرس قرارداد تولیدکننده
        address receiver;       // آدرس دریافت‌کننده (مثلاً بیمارستان)
        string status;          // وضعیت توزیع (Pending, In Transit, Delivered)
    }

    mapping(uint256 => Distribution) public distributions; // نگاشت ID توزیع‌ها
    uint256 public nextDistributionID;                     // شمارنده ID توزیع‌ها

    event DistributionCreated(
        uint256 distributionID,
        uint256 batchID,
        address manufacturer,
        address receiver,
        string status
    );

    event StatusUpdated(uint256 distributionID, string newStatus);

    // ایجاد یک توزیع جدید
    function createDistribution(
        uint256 batchID,
        address manufacturer,
        address receiver
    ) public {
        // بررسی اعتبار Batch
        require(validateBatch(manufacturer, batchID), "Invalid batch");

        // ثبت اطلاعات توزیع
        distributions[nextDistributionID] = Distribution(
            batchID,
            manufacturer,
            receiver,
            "Pending"
        );

        emit DistributionCreated(nextDistributionID, batchID, manufacturer, receiver, "Pending");
        nextDistributionID++;
    }

    // به‌روزرسانی وضعیت توزیع
    function updateStatus(uint256 distributionID, string memory newStatus) public {
        require(distributionID < nextDistributionID, "Invalid distribution ID");
        distributions[distributionID].status = newStatus;

        emit StatusUpdated(distributionID, newStatus);
    }

    // دریافت اطلاعات توزیع
    function getDistribution(uint256 distributionID)
        public
        view
        returns (
            uint256,
            address,
            address,
            string memory
        )
    {
        require(distributionID < nextDistributionID, "Invalid distribution ID");
        Distribution memory dist = distributions[distributionID];
        return (dist.batchID, dist.manufacturer, dist.receiver, dist.status);
    }

    // بررسی اعتبار Batch
    function validateBatch(address manufacturer, uint256 batchID) public view returns (bool) {
        DrugManufacturer manufacturerContract = DrugManufacturer(manufacturer);
        (, uint256 batchAmount, , string memory status) = manufacturerContract.getBatch(batchID);
        require(batchAmount > 0, "Invalid batch");
        return true;
    }
}
