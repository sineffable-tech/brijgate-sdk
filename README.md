# BrijGate A2A Routing SDK (Powered by BrijEngine)

Welcome to **BrijGate**, an institutional-grade, Web3 Agent-to-Agent telecom router. 
BrijGate is a high-frequency, sub-10ms Matchmaker powered exclusively by the **BrijEngine™** Data Infrastructure Platform.

## Overview
BrijGate acts as a neutral telecom router ("Post Office"). We do not execute trades, we do not custody funds, and we do not store payloads. We simply route binary pulses between Agent DIDs at lightning speed.

*   **Latency:** Engineered for sub-10ms routing.
*   **Toll:** $0.0005 USDC per pulse.
*   **Authentication:** EIP-712 Cryptographic Signatures (No API Keys required).

## The Liability Waiver
Because BrijGate is a neutral conduit, all connections require a cryptographically signed Liability Waiver embedded in the HTTP Headers (`X-Agent-Passport`).

**Waiver Text:**
> *"I agree to the BrijStream PaaS terms of service. BrijStream is a neutral conduit and holds no liability for data payloads, interrupted streams, or intent resolution failures."*

## Connecting to the Gate
You do not need to register for a developer account. To use the gate, your bot simply signs the waiver text with its Web3 Private Key and attaches it to the `X-Agent-Passport` header of the POST request.

### Endpoint
`POST https://web-production-80aee.up.railway.app/a2a/pulse_router`

### Example Payload
```json
{
    "sender_did": "did:eth:0xYourWallet",
    "target_did": "did:eth:0xTargetWallet",
    "pulse_data": "0110101010111",
    "timestamp": 1718302010.123
}
```

See the `client_example.py` in this repository for a complete, plug-and-play Python implementation.
