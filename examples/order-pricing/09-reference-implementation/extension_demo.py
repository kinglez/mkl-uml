"""Demo-only change exercise; this algorithm is not registered by production wiring."""
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

from pricing.adapters import build_port, default_registrations, InMemoryCatalog
from pricing.policies import require_subtotal

ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class CappedHalfDiscount:
    """New demo rule: half the item subtotal, capped at 2000 cents."""
    def discount(self, subtotal: int, currency: str) -> int:
        require_subtotal(subtotal, currency)
        return min(subtotal // 2, 2000)


def exercise():
    protected = ("pricing/service.py", "pricing/core.py")
    before = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in protected}
    oracle = json.loads((ROOT.parent / "00-input/acceptance-oracle.json").read_text(encoding="utf-8"))
    fixtures = deepcopy(oracle["fixtures"])
    fixtures["coupons"]["HALFCAP"] = {"kind": "capped_half", "minimumSubtotal": 0,
                                       "expiresAt": "2030-01-01T00:00:00Z"}
    catalog = InMemoryCatalog(fixtures["products"], fixtures["coupons"])
    request = deepcopy(oracle["cases"][0]["input"])
    baseline = build_port(catalog).handle(request)
    registrations = dict(default_registrations())
    registrations["capped_half"] = lambda coupon: CappedHalfDiscount()
    request["couponCode"] = "HALFCAP"
    input_before = deepcopy((request, fixtures, catalog.snapshot()))
    result = build_port(catalog, registrations).handle(request)
    after = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in protected}
    return {"change": "Add demo-only capped_half policy, trusted coupon fixture and registration",
            "baseline_result": baseline, "extension_result": result,
            "literal_expected_extension": {"ok": True, "subtotal": 25500, "discount": 2000,
                                           "payable": 23500, "currency": "CNY"},
            "protected_before_sha256": before, "protected_after_sha256": after,
            "protected_sources_unchanged": before == after,
            "inputs_unchanged": input_before == (request, fixtures, catalog.snapshot()),
            "limit": "Source stability and finite behavior examples; not a universal OCP/LSP proof."}


if __name__ == "__main__":
    evidence = exercise()
    expected = evidence["literal_expected_extension"]
    if (evidence["extension_result"] != expected or not evidence["protected_sources_unchanged"]
            or not evidence["inputs_unchanged"]):
        raise SystemExit("Extension exercise failed")
    target = ROOT / "evidence/extension.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2))
