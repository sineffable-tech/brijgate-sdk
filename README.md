# BrijGate A2A Trading SDK

Welcome to the **BrijGate SDK**, an institutional-grade, Web3 Agent-to-Agent routing engine. 
BrijGate empowers trading bots to execute high-frequency trades off-chain in `<10ms` while offering a revolutionary On-Chain Fallback router.

## 🚀 The Off-Chain Sprint (<10ms)
When you submit a trade via the SDK, BrijGate immediately searches its high-speed Matchmaker dark pool for a counterparty. 
If a match is found within **500 milliseconds**, the trade is executed entirely off-chain via cryptographic State Channel signatures. 
* **Latency:** < 10ms
* **Gas Fees:** $0
* **BrijGate Toll (Tier 1):** $0.0005 USDC per successful match.

## 📡 Tier 2: The WebSocket JIT Feed ($500/mo)
For professional Market Makers and MEV searchers, BrijGate offers a Tier 2 Subscription.
By connecting to our real-time WebSocket feed (`listen_for_intents()`), your bot will receive sub-millisecond "Blind Pings" the moment a new bot enters the lobby. 
This provides a massive mathematical advantage, allowing you to instantly pounce on incoming liquidity and guarantee a match within the 500ms window.
* **Subscription Fee:** $500.00 USDC / month (Automatically deducted from your BrijGate Escrow Ledger).
* **Subscription Bonus:** When you subscribe to Tier 2, your account is immediately credited with $50.00 in free toll credits (enough for 100,000 free trades!).

## ⚖️ Terms of Use & Live Billing
By utilizing the BrijGate SDK, you agree to the following Escrow Billing structure and terms:

1. **100% Live Environment:** The BrijGate router operates on strict real-money crypto principles. There are no free trial mock balances.
2. **Minimum Deposit Requirement:** You must have a minimum of **$1.00 USDC** deposited into the BrijGate Escrow Smart Contract on the Polygon network to execute an off-chain trade.
3. **Escrow Protection:** Your deposited Escrow balance is **never touched** unless a successful off-chain match occurs. You are not charged for open, unfilled, or cancelled intents.
4. **HTTP 402 Refusals:** If your Escrow balance falls below $1.00 (Tier 1) or you attempt to connect to the JIT Feed with less than $500 (Tier 2), the router will return an `HTTP 402 Payment Required` and refuse service until you deposit funds.
5. **Refund Policy (Cryptographic Withdrawals):** 
   - **Toll Deposits (Tier 1):** You may withdraw your unused Escrow balance at any time by submitting a cryptographically signed request to the BrijGate API (`POST /withdraw_escrow`). You must sign the message `"Withdraw {amount} USDC at {timestamp}"` using your private key. The API will cryptographically verify your identity and instantly refund the remaining on-chain USDC directly to your wallet.
   - **Subscriptions (Tier 2):** The $500.00 USDC monthly subscription fee is **strictly non-refundable** once the WebSocket connection has been established. If you request a refund within 30 days, it applies only to your *unspent Tier 1 toll balance*, not the subscription fee.
6. **Anti-Rug-Pull Guarantee:** Our `BrijGateEscrow.sol` Smart Contract mathematically segregates your active TVL (`totalDeposits`) from BrijStream's collected tolls (`accumulatedRevenue`). The `adminSweep` function is hardcoded to *only* withdraw from the revenue pool. Your Escrow deposits are mathematically immune to corporate rug-pulls.
7. **Limitation of Liability:** BrijStream is a neutral telecom routing provider. We do not guarantee trade profitability, execution speeds, or protection against MEV slippage on public networks. The SDK and Escrow contract are provided "AS-IS" without warranty. BrijStream is not liable for financial losses incurred due to network outages, misconfigured bots, or smart contract exploits.

## 📣 The On-Chain Fallback Billboard (Zero Friction)
BrijGate solves the "Cold Start" liquidity problem for you automatically. 

If the SDK cannot find an off-chain match within 500ms, it refuses to let you miss your trade. The SDK will automatically generate a Fallback Web3 transaction to execute your trade on public Automated Market Makers (like Uniswap) directly on Polygon.

**The Marketing Superpower:**
When the SDK falls back to the blockchain, it silently appends a hexadecimal Billboard string to the end of your transaction payload:
`LATENCY_TOO_HIGH? GET_BRIJGATE: github.com/BrijEngine/brijgate-sdk`

Because this data is permanently engraved on the blockchain, competing bots analyzing your on-chain trades will immediately see your advertisement. By simply using the SDK, you are actively converting your competitors and bringing more liquidity into the high-speed BrijGate dark pool!

---

## ⚡ Quickstart

Install the SDK and connect your bot with three lines of code. You do not need API keys; the SDK handles all cryptographic authentication using your Web3 wallet.

```python
import asyncio
from brijgate import BrijGateClient

async def main():
    # Initialize the SDK with your private key
    client = BrijGateClient(private_key="0xYourPrivateKey")
    
    # Submit your trade. The SDK handles the 500ms sprint and the Fallback Billboard automatically!
    result = await client.submit_trade(
        order_type="BUY_ORDER",
        asset="MTT_TOKEN",
        amount=500,
        payment="0.1_POL"
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

See `client_example.py` for more details.
