// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PharmacyAndHospital {
    struct Product {
        string name;
        uint256 amount;
    }

    mapping(uint256 => Product) public inventory; // ذخیره محصولات
    uint256 public nextProductID; // شناسه بعدی محصول

    address public distributor; // آدرس توزیع‌کننده

    event ProductReceived(uint256 productID, string name, uint256 amount);
    event ProductSold(uint256 productID, string name, uint256 amount);

    modifier onlyDistributor() {
        require(msg.sender == distributor, "Only distributor can call this");
        _;
    }

    constructor(address _distributor) {
        distributor = _distributor;
    }

    // دریافت محصول از توزیع‌کننده و افزودن به موجودی
    function receiveProduct(string memory name, uint256 amount) public onlyDistributor {
        inventory[nextProductID] = Product(name, amount);
        emit ProductReceived(nextProductID, name, amount);
        nextProductID++;
    }

    // فروش محصول
    function sellProduct(uint256 productID, uint256 amount) public {
        require(productID < nextProductID, "Invalid product ID");
        require(inventory[productID].amount >= amount, "Not enough stock");

        inventory[productID].amount -= amount;
        emit ProductSold(productID, inventory[productID].name, amount);
    }

    // مشاهده موجودی محصول
    function getProduct(uint256 productID) public view returns (string memory, uint256) {
        require(productID < nextProductID, "Invalid product ID");
        Product memory product = inventory[productID];
        return (product.name, product.amount);
    }
}
