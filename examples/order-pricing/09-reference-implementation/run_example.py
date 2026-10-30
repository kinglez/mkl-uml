"""Run visible CU-01 examples with trusted fixture setup, without a live service."""
from copy import deepcopy
import json
from pathlib import Path
from pricing.adapters import build_port, InMemoryCatalog

ROOT = Path(__file__).resolve().parent


def main():
    oracle = json.loads((ROOT.parent / "00-input/acceptance-oracle.json").read_text(encoding="utf-8"))
    fixtures = oracle["fixtures"]
    catalog = InMemoryCatalog(fixtures["products"], fixtures["coupons"])
    port = build_port(catalog)
    for code in (None, "SAVE30", "TENOFF", "BIGSAVE", "UNKNOWN-COUPON"):
        request = deepcopy(oracle["cases"][0]["input"])
        request["couponCode"] = code
        print(json.dumps({"coupon": code, "result": port.handle(request)}, ensure_ascii=False))
    request = deepcopy(oracle["cases"][0]["input"])
    request.update(couponCode="SAVE30", evaluatedAt="2030-01-01T00:00:00Z")
    print(json.dumps({"scenario": "exact expiry", "result": port.handle(request)}))


if __name__ == "__main__":
    main()
