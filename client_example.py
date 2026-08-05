import asyncio
import os
from brijgate import BrijGateClient

async def main():
    # In production, securely load your private key from environment variables
    # For testing, we use a dummy private key (do not use real funds with this!)
    PRIVATE_KEY = os.getenv("AGENT_PRIVATE_KEY", "0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef")
    
    print("Initializing BrijGate Trading SDK...")
    client = BrijGateClient(private_key=PRIVATE_KEY)
    
    # Tier 2 Market Maker Example:
    # 1. Start the WebSocket listener in the background to receive Blind Pings
    listener_task = asyncio.create_task(client.listen_for_intents())
    
    # 2. Wait a moment, then simulate another bot submitting a trade
    await asyncio.sleep(2)
    
    print("\n[Simulated Action] Submitting trade to the BrijGate...")
    result = await client.submit_trade(
        order_type="BUY_ORDER",
        asset="MTT_TOKEN",
        amount=500,
        payment="0.1_POL"
    )
    
    print(f"\nTrade Result:")
    print(result)
    
    # Let the listener run for a few more seconds to catch the ping
    await asyncio.sleep(2)
    listener_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
