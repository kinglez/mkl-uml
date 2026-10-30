"""Behavior tests, with independent literal expectations from the frozen oracle."""
from copy import deepcopy
from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import unittest

from pricing.adapters import build_port, default_registrations, InMemoryCatalog, QuoteRequestPort
from pricing.core import Cart, CartLine, Coupon, PriceQuote, Refusal
from pricing.policies import NoDiscount, FixedDiscount, PercentageDiscount, RegistryPolicyResolver
from pricing.service import QuoteService

ROOT = Path(__file__).resolve().parents[1]
ORACLE = json.loads((ROOT.parent / "00-input/acceptance-oracle.json").read_text(encoding="utf-8"))


def merge(base, changes):
    result = deepcopy(base)
    for key, value in changes.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def setup(overrides=None):
    fixtures = merge(ORACLE["fixtures"], overrides or {})
    catalog = InMemoryCatalog(fixtures["products"], fixtures["coupons"])
    port = build_port(catalog)
    return fixtures, catalog, port


class WorkflowTests(unittest.TestCase):
    def test_independent_30_case_oracle_repeated_read_only(self):
        self.assertEqual(30, len(ORACLE["cases"]))
        for case in ORACLE["cases"]:
            with self.subTest(case=case["caseID"], scenario=case["scenario"]):
                fixtures, catalog, port = setup(case.get("fixtureOverrides"))
                request = deepcopy(case["input"])
                before = deepcopy((request, fixtures, catalog.snapshot()))
                first = port.handle(request)
                self.assertEqual(case["expected"], first)
                self.assertEqual(before, (request, fixtures, catalog.snapshot()))
                second = port.handle(request)
                self.assertEqual(case["expected"], second)
                self.assertEqual(first, second)
                self.assertEqual(before, (request, fixtures, catalog.snapshot()))
                if not first["ok"]:
                    self.assertEqual({"ok", "reasonCategory"}, set(first))

    def assert_refused(self, request_changes=None, overrides=None, reason=None):
        fixtures, catalog, port = setup(overrides)
        request = merge(ORACLE["cases"][0]["input"], request_changes or {})
        before = deepcopy((request, fixtures, catalog.snapshot()))
        result = port.handle(request)
        self.assertEqual({"ok": False, "reasonCategory": reason}, result)
        self.assertEqual(before, (request, fixtures, catalog.snapshot()))

    def test_FE03_invalid_product_price_and_currency(self):
        for value in (-1, 1.25, True, None):
            with self.subTest(price=value):
                self.assert_refused(overrides={"products": {"BOOK-001": {"unitPrice": value}}},
                                    reason="INVALID_PRODUCT_CONFIGURATION")
        self.assert_refused(overrides={"products": {"BOOK-001": {"currency": "USD"}}},
                            reason="INVALID_PRODUCT_CONFIGURATION")

    def test_FE07_invalid_fixed_configuration(self):
        for value in (True, None, "3000"):
            with self.subTest(amount=value):
                self.assert_refused({"couponCode": "SAVE30"},
                                    {"coupons": {"SAVE30": {"fixedAmount": value}}},
                                    "INVALID_COUPON_CONFIGURATION")

    def test_FE07_invalid_rate_configuration(self):
        for value in (True, None, 1.5, "1000"):
            with self.subTest(rate=value):
                self.assert_refused({"couponCode": "TENOFF"},
                                    {"coupons": {"TENOFF": {"basisPoints": value}}},
                                    "INVALID_COUPON_CONFIGURATION")

    def test_FE07_invalid_common_configuration(self):
        for change in ({"minimumSubtotal": 1.5}, {"minimumSubtotal": True},
                       {"minimumSubtotal": None}, {"currency": "USD"},
                       {"expiresAt": "invalid"}, {"expiresAt": "2030-01-01T00:00:00"},
                       {"expiresAt": "2030-01-01T00:00:00+08:00"}, {"kind": "unregistered"}):
            with self.subTest(change=change):
                self.assert_refused({"couponCode": "SAVE30"}, {"coupons": {"SAVE30": change}},
                                    "INVALID_COUPON_CONFIGURATION")

    def test_FE01_missing_naive_invalid_and_non_UTC_time(self):
        for value in (None, "invalid", "2026-10-29T00:00:00", "2026-10-29T00:00:00+08:00", True):
            with self.subTest(time=value):
                self.assert_refused({"evaluatedAt": value}, reason="INVALID_EVALUATION_TIME")
        _, _, port = setup()
        request = deepcopy(ORACLE["cases"][0]["input"])
        del request["evaluatedAt"]
        self.assertEqual({"ok": False, "reasonCategory": "INVALID_EVALUATION_TIME"}, port.handle(request))

    def test_adapter_ignores_untrusted_presented_price(self):
        _, catalog, port = setup()
        request = deepcopy(ORACLE["cases"][0]["input"])
        request["cart"][0]["unitPrice"] = 1
        request["products"] = {"BOOK-001": {"unitPrice": 1, "currency": "CNY"}}
        before = deepcopy((request, catalog.snapshot()))
        self.assertEqual(ORACLE["cases"][0]["expected"], port.handle(request))
        self.assertEqual(before, (request, catalog.snapshot()))

    def test_catalog_is_a_detached_snapshot(self):
        fixtures, catalog, port = setup()
        fixtures["products"]["BOOK-001"]["unitPrice"] = 1
        snapshot = catalog.snapshot()
        snapshot["products"]["BOOK-001"]["unitPrice"] = 2
        self.assertEqual(ORACLE["cases"][0]["expected"], port.handle(ORACLE["cases"][0]["input"]))
        self.assertEqual(12000, catalog.snapshot()["products"]["BOOK-001"]["unitPrice"])

    def test_FA03_zero_subtotal_preserves_coupon_conditions(self):
        override = {"products": {"FREE": {"unitPrice": 0, "currency": "CNY"}}}
        request = {"cart": [{"productCode": "FREE", "quantity": 1}], "couponCode": "SAVE30"}
        self.assert_refused(request, override, "COUPON_MINIMUM_NOT_REACHED")
        _, _, port = setup(merge(override, {"coupons": {"SAVE30": {"minimumSubtotal": 0}}}))
        full = merge(ORACLE["cases"][0]["input"], request)
        self.assertEqual({"ok": True, "subtotal": 0, "discount": 0, "payable": 0, "currency": "CNY"},
                         port.handle(full))

    def test_eligibility_refusal_does_not_invoke_discount(self):
        class SpyPolicy:
            calls = 0
            def discount(self, subtotal, currency):
                self.calls += 1
                return 0
        policy = SpyPolicy()
        _, catalog, _ = setup()
        resolver = RegistryPolicyResolver({"fixed": lambda coupon: policy})
        port = QuoteRequestPort(QuoteService(catalog, catalog, resolver))
        request = merge(ORACLE["cases"][0]["input"],
                        {"couponCode": "SAVE30", "evaluatedAt": "2030-01-01T00:00:00Z"})
        self.assertEqual({"ok": False, "reasonCategory": "EXPIRED_COUPON"}, port.handle(request))
        self.assertEqual(0, policy.calls)

    def test_policy_contract_violation_cannot_produce_a_quote(self):
        class BadPolicy:
            def __init__(self, value): self.value = value
            def discount(self, subtotal, currency): return self.value
        for value in (-1, 25501, True, 0.5):
            with self.subTest(value=value):
                _, catalog, _ = setup()
                resolver = RegistryPolicyResolver({"fixed": lambda coupon: BadPolicy(value)})
                port = QuoteRequestPort(QuoteService(catalog, catalog, resolver))
                request = merge(ORACLE["cases"][0]["input"], {"couponCode": "SAVE30"})
                self.assertEqual({"ok": False, "reasonCategory": "POLICY_CONTRACT_VIOLATION"}, port.handle(request))

    def test_domain_results_are_immutable(self):
        quote = PriceQuote(25500, 3000, 22500, "CNY")
        with self.assertRaises(FrozenInstanceError): quote.payable = 0
        with self.assertRaises(Refusal): PriceQuote(25500, 3000, 22000, "CNY")
        line = CartLine("PEN-002", 1)
        with self.assertRaises(FrozenInstanceError): line.quantity = 3


class PolicyContractTests(unittest.TestCase):
    def assert_contract(self, policy, subtotal, currency, expected):
        before = deepcopy(vars(policy))
        first = policy.discount(subtotal, currency)
        second = policy.discount(subtotal, currency)
        self.assertEqual(expected, first)
        self.assertEqual(first, second)
        self.assertIs(type(first), int)
        self.assertGreaterEqual(first, 0)
        self.assertLessEqual(first, subtotal)
        self.assertEqual(before, vars(policy))
        self.assertEqual("CNY", currency)

    def test_shared_independent_policy_vectors(self):
        policies = {"none": NoDiscount(), "fixed3000": FixedDiscount(3000),
                    "percentage1000": PercentageDiscount(1000), "fixed50000": FixedDiscount(50000)}
        for vector in ORACLE["policyContract"]["vectors"]:
            for name, policy in policies.items():
                with self.subTest(subtotal=vector["subtotal"], policy=name):
                    self.assert_contract(policy, vector["subtotal"], vector["currency"],
                                         vector["expectedDiscounts"][name])

    def test_all_policies_share_invalid_input_preconditions(self):
        from extension_demo import CappedHalfDiscount
        for policy in (NoDiscount(), FixedDiscount(3000), PercentageDiscount(1000), CappedHalfDiscount()):
            for subtotal, currency in ((-1, "CNY"), (True, "CNY"), (0.5, "CNY"), (333, "USD")):
                with self.subTest(policy=type(policy).__name__, subtotal=subtotal, currency=currency):
                    with self.assertRaises(ValueError): policy.discount(subtotal, currency)

    def test_extension_shared_contract_and_workflow_stability(self):
        from extension_demo import CappedHalfDiscount, exercise
        for subtotal, expected in ((0, 0), (333, 166), (25500, 2000)):
            with self.subTest(subtotal=subtotal):
                self.assert_contract(CappedHalfDiscount(), subtotal, "CNY", expected)
        evidence = exercise()
        self.assertEqual({"ok": True, "subtotal": 25500, "discount": 2000,
                          "payable": 23500, "currency": "CNY"}, evidence["extension_result"])
        self.assertEqual(evidence["protected_before_sha256"], evidence["protected_after_sha256"])
        self.assertTrue(evidence["protected_sources_unchanged"])


if __name__ == "__main__":
    unittest.main()
