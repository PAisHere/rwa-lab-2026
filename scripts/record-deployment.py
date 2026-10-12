"""Record actual CREATE addresses; explorer verification must be reviewed separately."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
run = root / "broadcast/Deploy.s.sol/11155111/run-latest.json"
data = json.loads(run.read_text())
names = ["MockUSDC", "ComplianceRegistry", "MockPriceFeed", "TBillToken",
         "MockTBillCustodian", "TBillVault", "RedemptionQueue"]
addresses = {tx["contractName"]: tx["contractAddress"] for tx in data["transactions"]
             if tx.get("transactionType") == "CREATE"}
if any(name not in addresses for name in names):
    raise SystemExit("Missing a required deployment; do not record an incomplete broadcast.")
lines = ["## Deployment (Sepolia)", "", "Ethereum Sepolia, chain ID 11155111.", "",
         "Addresses recorded from the actual broadcast. Check each explorer page for source verification.",
         "", "| Contract | Address | Etherscan |", "|---|---|---|"]
for name in names:
    address = addresses[name]
    lines.append(f"| {name} | `{address}` | [Source](https://sepolia.etherscan.io/address/{address}#code) |")
p = root / "README.md"
text = p.read_text(encoding="utf-8")
start = text.index("## Deployment (Sepolia)")
end = text.find("\n## ", start + 1)
if end == -1:
    end = len(text)
p.write_text(text[:start] + "\n".join(lines) + "\n" + text[end:], encoding="utf-8")
print("Recorded seven addresses in README.md; confirm all seven show verified source.")
