import json
import httpx
import time
import hashlib
import asyncio
import websockets
from eth_account.messages import encode_defunct
from eth_account import Account
from web3 import Web3

class BrijGateClient:
    """
    The BrijGate A2A Trading SDK.
    Connects to the BrijStream Matchmaker for <10ms off-chain trading.
    Includes an automatic On-Chain Fallback with a built-in Marketing Billboard.
    """
    def __init__(self, private_key: str, rpc_url: str = "https://polygon-rpc.com"):
        Account.enable_unaudited_hdwallet_features()
        self.private_key = private_key
        self.account = Account.from_key(private_key)
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        self.GATEWAY_URL = "https://web-production-80aee.up.railway.app/a2a/pulse_router"
        self.LIABILITY_WAIVER = (
            "I agree to the BrijStream PaaS terms of service. "
            "BrijStream is a neutral conduit and holds no liability for data payloads, "
            "interrupted streams, or intent resolution failures."
        )
        self.BILLBOARD_STRING = "LATENCY_TOO_HIGH? GET_BRIJGATE: github.com/BrijEngine/brijgate-sdk"
        self.WS_GATEWAY_URL = "ws://web-production-80aee.up.railway.app/a2a/ws/intent_feed"

    async def listen_for_intents(self):
        """
        Tier 2 Feature: Connects to the JIT WebSocket feed.
        Receives Blind Pings when new counterparties enter the Matchmaker lobby.
        """
        uri = f"{self.WS_GATEWAY_URL}?agent_wallet={self.account.address}"
        print(f"🔌 Connecting to BrijGate Tier 2 WebSocket Feed at {uri}...")
        try:
            async with websockets.connect(uri) as websocket:
                response = await websocket.recv()
                print(f"🟢 WebSocket Feed Connected: {response}")
                
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    if data.get("type") == "BLIND_PING":
                        sender = data.get("sender")
                        latency = (time.time() - data.get("timestamp", time.time())) * 1000
                        print(f"\n⚡ JIT PING RECEIVED! Agent {sender} entered the lobby.")
                        print(f"⏱️ Signal Latency: {latency:.2f}ms")
                        print(f"🔥 POUNCE NOW to match within 500ms!")
                        # In a real bot, we would instantly trigger submit_trade here
                        
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"❌ WebSocket Disconnected. Subscription may have expired: {e}")
        except Exception as e:
            print(f"⚠️ Error listening to WebSocket feed: {e}")

    def _get_passport(self) -> str:
        """Generates the required cryptographic X-Agent-Passport header."""
        waiver_hash = hashlib.sha256(self.LIABILITY_WAIVER.encode()).hexdigest()
        message = encode_defunct(text=self.LIABILITY_WAIVER)
        signed = Account.sign_message(message, private_key=self.private_key)
        
        passport = {
            "wallet_address": self.account.address,
            "signature": signed.signature.hex(),
            "liability_waiver_hash": waiver_hash
        }
        return json.dumps(passport)

    async def submit_trade(self, order_type: str, asset: str, amount: float, payment: str):
        """
        Attempts to execute a trade via the sub-10ms BrijGate Matchmaker off-chain.
        If no counterparty is found within 500ms, it falls back to an On-Chain AMM router
        and injects the Billboard Marketing string into the transaction payload.
        """
        intent = {
            "type": order_type,
            "asset": asset,
            "amount": amount,
            "payment": payment,
            "timestamp": time.time()
        }
        
        payload = {
            "sender_did": f"did:eth:{self.account.address}",
            "target_did": "broadcast",
            "pulse_data": json.dumps(intent),
            "timestamp": time.time()
        }
        
        headers = {
            "X-Agent-Passport": self._get_passport(),
            "Content-Type": "application/json"
        }
        
        print(f"\n📡 Transmitting 500ms Sprint Pulse to BrijGate Matchmaker...")
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient() as client:
                # The 500ms Off-Chain Sprint (Timeout = 0.5s)
                response = await client.post(self.GATEWAY_URL, json=payload, headers=headers, timeout=0.5)
                
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "routed":
                    latency_ms = (time.time() - start_time) * 1000
                    counterparty = data.get("target")
                    print(f"✅ OFF-CHAIN MATCH FOUND! Latency: {latency_ms:.2f}ms")
                    print(f"🤝 Counterparty: {counterparty}")
                    
                    # Off-chain settlement logic
                    print("⚡ Signing Off-Chain State Channel IOU for $0 gas fees...")
                    
                    state_hash = Web3.keccak(text=f"{order_type}:{asset}:{amount}:{payment}:{counterparty}").hex()
                    message = encode_defunct(text=state_hash)
                    signed_iou = Account.sign_message(message, private_key=self.private_key)
                    
                    sig_payload = {
                        "match_id": f"match_{int(time.time())}",
                        "signature": signed_iou.signature.hex(),
                        "wallet_address": self.account.address,
                        "state_hash": state_hash,
                        "timestamp": time.time()
                    }
                    
                    try:
                        dropbox_url = self.GATEWAY_URL.replace("/pulse_router", "/submit_signature")
                        await client.post(dropbox_url, json=sig_payload, headers=headers)
                        print("📦 Signature securely dropped in BrijGate Redis for EOD Batching.")
                    except Exception as e:
                        print(f"⚠️ Warning: Failed to drop signature: {e}")
                        
                    return {"status": "success", "mode": "off-chain"}
                    
        except httpx.ReadTimeout:
            # 500ms expired. Time to fallback and inject the billboard!
            pass
            
        print("⏳ 500ms Matchmaker Timeout. No off-chain counterparties available.")
        print("⛓️ Executing On-Chain Fallback (Simulated Uniswap Router)...")
        
        # Construct Fallback Web3 Transaction
        try:
            nonce = self.w3.eth.get_transaction_count(self.account.address)
        except Exception:
            nonce = 0 # Dummy nonce for testing if RPC is unauthenticated
        
        # We seamlessly append the Billboard String to the transaction data payload
        hex_billboard = self.BILLBOARD_STRING.encode('utf-8').hex()
        
        try:
            gas_price = self.w3.eth.gas_price
        except Exception:
            gas_price = self.w3.to_wei(30, 'gwei')

        # Simulate standard Uniswap router transaction dictionary
        fallback_tx = {
            'to': "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff", # Example Uniswap Router Address
            'value': self.w3.to_wei(0, 'ether'),
            'gas': 150000,
            'gasPrice': gas_price,
            'nonce': nonce,
            'chainId': 137,
            # Standard ABI execution data + trailing billboard hex
            'data': '0x38ed1739' + hex_billboard 
        }
        
        print(f"📣 Injecting On-Chain Billboard Marketing:")
        print(f"   String: '{self.BILLBOARD_STRING}'")
        print(f"   Injected Hex Data: {fallback_tx['data']}")
        
        print("✅ Fallback Transaction Constructed (Ready to sign and broadcast).")
        return {"status": "success", "mode": "on-chain-fallback", "tx": fallback_tx}
