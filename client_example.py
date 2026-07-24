import json
import httpx
import time
import hashlib
from eth_account.messages import encode_defunct
from eth_account import Account

# --- 1. Your Bot Configuration ---
# In production, load your private key securely from environment variables.
# This wallet must have at least $0.0005 USDC to pay the pulse toll.
PRIVATE_KEY = "0x..." 
account = Account.from_key(PRIVATE_KEY)

# --- 2. BrijGate Details ---
GATEWAY_URL = "https://<YOUR_RAILWAY_URL>/a2a/pulse_router"
LIABILITY_WAIVER_TEXT = (
    "I agree to the BrijStream PaaS terms of service. "
    "BrijStream is a neutral conduit and holds no liability for data payloads, "
    "interrupted streams, or intent resolution failures."
)

def construct_passport_header():
    """Generates the cryptographic X-Agent-Passport header."""
    # 1. Hash the liability waiver
    waiver_hash = hashlib.sha256(LIABILITY_WAIVER_TEXT.encode()).hexdigest()
    
    # 2. Cryptographically sign the waiver using your Web3 Private Key
    message = encode_defunct(text=LIABILITY_WAIVER_TEXT)
    signed_message = Account.sign_message(message, private_key=PRIVATE_KEY)
    
    # 3. Construct the JSON header
    passport = {
        "wallet_address": account.address,
        "signature": signed_message.signature.hex(),
        "liability_waiver_hash": waiver_hash
    }
    return json.dumps(passport)

async def send_pulse(target_did: str, binary_payload: str):
    """Routes a high-frequency pulse through BrijGate."""
    payload = {
        "sender_did": f"did:eth:{account.address}",
        "target_did": target_did,
        "pulse_data": binary_payload,
        "timestamp": time.time()
    }
    
    headers = {
        "X-Agent-Passport": construct_passport_header()
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(GATEWAY_URL, json=payload, headers=headers)
        return response.json()

# --- Example Usage ---
# import asyncio
# asyncio.run(send_pulse("did:eth:0xTargetWallet", "010101010111"))
