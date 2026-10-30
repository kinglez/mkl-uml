/* HEADERS GENERATED FOR INSPECTION - CDR-01
 * Review instrument, NOT production code.
 * Generated from: 07-class-model/classes.puml
 * Review the model and conversion diagnostics before correcting the source.
 * Gaps are marked with ???; review all unresolved or unsupported syntax.
 * List/Optional preserve multiplicity; exact bounds remain in comments. */

public class Cart {
    private List<CartLine> linesCartLine;  // multiplicity 0..*; source multiplicity 0..*

    public void validate() { }
    public int subtotal(Map<String,Product> products, String currency) { }
}

public class CartLine {
    public String productCode;
    public int quantity;

}

public class Product {
    public String code;
    public int unitPrice;
    public String currency;

}

public class Coupon {
    public String code;
    public String kind;
    public int minimumSubtotal;
    public DateTime expiresAt;
    public String currency;
    public Map<String,Object> config;

    public void check_eligibility(int subtotal, DateTime evaluatedAt, String currency) { }
}

public class PriceQuote {
    public int subtotal;
    public int discount;
    public int payable;
    public String currency;

}

public interface ProductCatalog {  // <<solucion>>
    public Optional<Product> lookup_product(String code);
}

public interface CouponCatalog {  // <<solucion>>
    public Optional<Coupon> lookup_coupon(String code);
}

public interface PolicyResolver {  // <<solucion>>
    public DiscountPolicy resolve(Optional<Coupon> coupon);
}

public interface DiscountPolicy {  // <<solucion>>
    public int discount(int subtotal, String currency);
}

public class NoDiscount implements DiscountPolicy {  // <<solucion>>
    public int discount(int subtotal, String currency) { }
}

public class FixedDiscount implements DiscountPolicy {  // <<solucion>>
    public int amount;

    public int discount(int subtotal, String currency) { }
}

public class PercentageDiscount implements DiscountPolicy {  // <<solucion>>
    public int basisPoints;

    public int discount(int subtotal, String currency) { }
}

public class QuoteService {  // <<solucion>>
    private ProductCatalog product_catalog;
    private CouponCatalog coupon_catalog;
    private PolicyResolver policy_resolver;

    public PriceQuote quote(Cart cart, String currency, Optional<String> couponCode, DateTime evaluatedAt) { }
}

public class Refusal {  // <<solucion>>
    public String reasonCategory;

}

public class QuoteRequestPort {  // <<solucion>>
    private QuoteService service;

    public Map<String,Object> handle(Map<String,Object> request) { }
}

public class InMemoryCatalog implements CouponCatalog, ProductCatalog {  // <<solucion>>
    private Map<String,Object> products;
    private Map<String,Object> coupons;

    public Optional<Product> lookup_product(String code) { }
    public Optional<Coupon> lookup_coupon(String code) { }
    public Map<String,Object> snapshot() { }
}

public class RegistryPolicyResolver implements PolicyResolver {  // <<solucion>>
    private Map<String,PolicyFactory> registrations;

    public DiscountPolicy resolve(Optional<Coupon> coupon) { }
}

