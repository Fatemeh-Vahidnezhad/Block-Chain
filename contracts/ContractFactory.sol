// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./DrugManufacturer.sol";
import "./Distributor.sol";
import "./PharmacyAndHospital.sol";

contract ContractFactory {
    struct ManufacturerInfo {
        address manufacturerAddress;
        address owner;
    }

    struct DistributorInfo {
        address distributorAddress;
        address owner;
    }

    ManufacturerInfo[] public manufacturers;
    DistributorInfo[] public distributors;
    address[] public hospitals; // لیست بیمارستان‌ها
    address[] public pharmacies; // لیست داروخانه‌ها
	
	
    event ManufacturerCreated(address indexed manufacturerAddress, address indexed owner);
    event DistributorCreated(address indexed distributorAddress, address indexed owner);
	event HospitalCreated(address indexed hospitalAddress, address indexed owner);
    event PharmacyCreated(address indexed pharmacyAddress, address indexed owner);

    // ایجاد قرارداد تولیدکننده
    function createManufacturer() public {
        DrugManufacturer manufacturer = new DrugManufacturer();
        manufacturers.push(ManufacturerInfo(address(manufacturer), msg.sender));
        emit ManufacturerCreated(address(manufacturer), msg.sender);
    }

    // ایجاد قرارداد توزیع‌کننده
    function createDistributor() public {
        Distributor distributor = new Distributor();
        distributors.push(DistributorInfo(address(distributor), msg.sender));
        emit DistributorCreated(address(distributor), msg.sender);
    }

    // دریافت تعداد قراردادهای تولیدکننده
    function getManufacturerCount() public view returns (uint256) {
        return manufacturers.length;
    }

    // دریافت تعداد قراردادهای توزیع‌کننده
    function getDistributorCount() public view returns (uint256) {
        return distributors.length;
    }

    // دریافت آدرس قرارداد تولیدکننده بر اساس ایندکس
    function getManufacturer(uint256 index) public view returns (address) {
        require(index < manufacturers.length, "Index out of range");
        return manufacturers[index].manufacturerAddress;
    }

    // دریافت آدرس قرارداد توزیع‌کننده بر اساس ایندکس
    function getDistributor(uint256 index) public view returns (address) {
        require(index < distributors.length, "Index out of range");
        return distributors[index].distributorAddress;
    }

    // ایجاد بیمارستان
    function createHospital(address distributor) public {
        PharmacyAndHospital hospital = new PharmacyAndHospital(distributor);
        hospitals.push(address(hospital));
        emit HospitalCreated(address(hospital), msg.sender);
    }

    // ایجاد داروخانه
    function createPharmacy(address distributor) public {
        PharmacyAndHospital pharmacy = new PharmacyAndHospital(distributor);
        pharmacies.push(address(pharmacy));
        emit PharmacyCreated(address(pharmacy), msg.sender);
    }

    // دریافت آدرس بیمارستان‌ها
    function getHospitals() public view returns (address[] memory) {
        return hospitals;
    }

    // دریافت آدرس داروخانه‌ها
    function getPharmacies() public view returns (address[] memory) {
        return pharmacies;
    }
}
