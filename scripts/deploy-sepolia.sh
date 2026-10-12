#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# Load local credentials without putting the signing key in command arguments.
if [[ -f .env ]]; then
    set -a
    source .env
    set +a
fi
: "${PRIVATE_KEY:?Set PRIVATE_KEY in .env}"
: "${SEPOLIA_RPC_URL:?Set SEPOLIA_RPC_URL in .env}"
: "${ETHERSCAN_API_KEY:?Set ETHERSCAN_API_KEY in .env}"
chain=$(cast chain-id --rpc-url "$SEPOLIA_RPC_URL")
[[ "$chain" == "11155111" ]] || { echo "RPC is not Ethereum Sepolia" >&2; exit 1; }
forge script script/Deploy.s.sol:Deploy --rpc-url "$SEPOLIA_RPC_URL" \
    --chain 11155111 --broadcast --verify --etherscan-api-key "$ETHERSCAN_API_KEY" "$@"
echo "Review verification results, then run: python3 scripts/record-deployment.py"
