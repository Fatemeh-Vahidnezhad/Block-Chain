from brownie import network

def main():
    print(f"Active network: {network.show_active()}")
