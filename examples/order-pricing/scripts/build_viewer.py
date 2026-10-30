"""Build a dependency-free, offline reading view from this example's actual files."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
STAGES = [
    ("01-domain", "1 · Domain model", "Establish business concepts and relationships before selecting implementation strategies.", ["domain.puml", "glossary.md"]),
    ("02-use-cases", "2 · Use cases", "Identify the user goal, system boundary and participating external role.", ["use-cases.puml", "actor-goal-map.md"]),
    ("03-spec", "3 · Specification", "Define basic, alternative and exception behavior with observable outcomes.", ["CU01-quote-cart.md", "interface-contract.md", "pdr-corrections.md"]),
    ("04-robustness", "4 · Robustness", "Connect behavior to boundaries, control responsibilities and domain entities. Analysis controls do not prescribe implementation classes.", ["robustness.puml", "correspondence.md"]),
    ("05-pdr", "5 · PDR", "Review analysis independently, resolve findings and record the technical basis for detailed design.", ["PDR-01.md"]),
    ("06-interactions", "6 · Interactions and tests", "Read the PDR outcome, allocate behavior to collaborators and derive tests from observable results.", ["operation-delta.md", "test-plan.md", "DESIGN_DECISIONS.md"]),
    ("07-class-model", "7 · Design classes", "Inspect types, operation allocation, source dependencies and concrete SOLID evidence.", ["classes.puml", "provenance.md", "SOLID.md"]),
    ("08-cdr", "8 · CDR", "Review static and dynamic design, requirements, test evidence and generated declarations.", ["CDR-01.md", "headers.java", "header-inspection.md"]),
]


def link(path, title=None):
    destination = Path(path).as_posix()
    return '<a href="' + escape(destination, quote=True) + '">' + escape(title or destination) + '</a>'


def main():
    result_path = ROOT / "validation/latest/result.json"
    if not result_path.exists():
        result_path = ROOT / "VALIDATION.json"
    result = json.loads(result_path.read_text(encoding="utf-8")) if result_path.exists() else {}
    verdict = "Verification passed" if result.get("passed") else "Verification pending; see the review records"
    counts = (str(result.get("reference_unittest_methods", "pending")) + " test methods · "
              + str(result.get("diagrams", "pending")) + " UML diagrams")
    nav = []
    panels = []
    for index, (directory, title, purpose, resources) in enumerate(STAGES):
        ident = "stage-" + str(index + 1)
        nav.append('<button data-target="' + ident + '" aria-selected="false">' + escape(title) + '</button>')
        files = [link(Path(directory) / name) for name in resources if (ROOT / directory / name).is_file()]
        images = []
        current = [Path(name).with_suffix(".svg").name for name in resources if name.endswith(".puml")]
        if directory == "06-interactions":
            current = [path.with_suffix(".svg").name for path in sorted((ROOT / directory).glob("*.puml"))]
        for name in current:
            path = ROOT / directory / name
            if not path.is_file():
                continue
            svg = path.read_text(encoding="utf-8")
            start = svg.find("<svg")
            if start >= 0:
                svg = svg[start:]
                # Inline each rendered diagram; no CDN, web request or external renderer.
                images.append('<figure><figcaption>' + escape(path.stem)
                              + ' <button class="fit" aria-pressed="false">Fit to width</button>'
                              + ' <a href="' + escape(path.relative_to(ROOT).as_posix())
                              + '">Open SVG</a></figcaption><div class="diagram">'
                              + svg + '</div></figure>')
        panels.append('<section id="' + ident + '" class="panel" hidden><h2>' + escape(title) + '</h2><p>'
                      + escape(purpose) + '</p><div class="files">' + "".join(files) + '</div>'
                      + "".join(images) + '</section>')
    content = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>MKL UML · Order pricing reference example</title>
<style>
:root{color-scheme:light dark;--bg:#f4f6fa;--card:#fff;--fg:#17243a;--muted:#52627b;--line:#d7dfec;--accent:#245bc7}
@media(prefers-color-scheme:dark){:root{--bg:#111823;--card:#1b2636;--fg:#edf2fc;--muted:#bbc7d9;--line:#384b65;--accent:#91b4ff}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.7 system-ui,-apple-system,sans-serif}
main{max-width:1280px;margin:auto;padding:32px 22px 72px}h1{font-size:32px;line-height:1.25;margin:0 0 14px}h2{font-size:22px;margin:0 0 10px}
p{margin:10px 0;color:var(--muted)}a{color:var(--accent);text-underline-offset:3px}.meta{font-size:14px}.badge{display:inline-block;background:var(--card);padding:6px 12px;border:1px solid var(--line);border-radius:6px;margin:4px 8px 4px 0}
nav{display:flex;flex-wrap:wrap;gap:8px;margin:24px 0}button{font:inherit;background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:9px 14px;cursor:pointer}button[aria-selected=true]{background:var(--accent);color:var(--bg)}button:focus-visible,a:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
.panel,.intro,.execution{background:var(--card);padding:24px;border:1px solid var(--line);border-radius:10px;margin-bottom:20px}.files{display:flex;flex-wrap:wrap;gap:12px;font-size:14px;margin:18px 0}.files a{overflow-wrap:anywhere}
figure{margin:24px 0 0}figcaption{font-size:14px;color:var(--muted);margin-bottom:8px}figcaption button{font-size:13px;padding:3px 9px;margin:0 10px}.diagram{overflow:auto;background:#fff;border:1px solid var(--line);border-radius:6px;padding:14px}.diagram svg{display:block;max-width:none;height:auto!important;margin:auto}.diagram.fit-width svg{width:100%!important;height:auto!important;max-width:100%}
table{border-collapse:collapse;width:100%;margin-top:14px}th,td{text-align:left;border-bottom:1px solid var(--line);padding:9px}code,pre{font:14px/1.6 ui-monospace,monospace}pre{overflow:auto;background:var(--bg);padding:16px;border-radius:6px}.note{border-left:4px solid var(--accent);padding-left:14px}
@media(max-width:640px){main{padding:24px 14px}.panel,.intro,.execution{padding:18px}h1{font-size:27px}button{padding:8px 10px}}
</style><main>
<h1>MKL UML · Order pricing</h1><p>A complete reference example: business rules, eight UML workflow stages, independent review findings, executable code and literal acceptance expectations.</p>
<div class="meta"><span class="badge">Validator baseline v1.0.2</span><span class="badge">__VERDICT__</span><span class="badge">__COUNTS__</span></div>
<div class="intro"><h2>The problem</h2><p>A Shopper submits product codes, quantities and an optional coupon. The system reads trusted catalog prices and returns the subtotal, discount and payable item amount, or an explicit refusal. The example is read-only and requires no external service.</p>
<table><thead><tr><th>Subtotal</th><th>Coupon rule</th><th>Payable</th></tr></thead><tbody><tr><td>CNY 255.00</td><td>No coupon</td><td>CNY 255.00</td></tr><tr><td>CNY 255.00</td><td>SAVE30: CNY 30 off orders of CNY 200 or more</td><td>CNY 225.00</td></tr><tr><td>CNY 255.00</td><td>TENOFF: 10% off orders of CNY 100 or more</td><td>CNY 229.50</td></tr><tr><td>CNY 255.00</td><td>BIGSAVE: CNY 500 off, capped at the subtotal</td><td>CNY 0.00</td></tr></tbody></table>
<p class="note">Money uses integer cents. Policies are teaching assumptions. AI technical reviews and passing tests provide bounded evidence; formal human/business acceptance remains Not fully verified.</p>
<div class="files">__TOP_LINKS__</div></div>
<nav aria-label="Eight workflow stages">__NAV__</nav>__PANELS__
<section class="execution"><h2>Run it locally</h2><p>From the repository root, Python's standard library runs the validators and reference tests. Add --render to regenerate SVG/PNG using PlantUML installed locally.</p>
<pre>python3 examples/order-pricing/09-reference-implementation/run_example.py
python3 examples/order-pricing/scripts/verify.py
python3 examples/order-pricing/scripts/verify.py --render</pre>
<p>The README explains execution, review boundaries and each stage's artifacts. This offline reader uses embedded diagrams and requires no CDN or hosted renderer.</p></section>
</main><script>
const tabs=[...document.querySelectorAll('nav button')];
function select(id){if(!document.getElementById(id))id='stage-1';for(const t of tabs)t.setAttribute('aria-selected',String(t.dataset.target===id));for(const p of document.querySelectorAll('.panel'))p.hidden=p.id!==id;}
tabs.forEach(t=>t.addEventListener('click',()=>{history.replaceState(null,'','#'+t.dataset.target);select(t.dataset.target)}));
document.querySelectorAll('button.fit').forEach(b=>b.addEventListener('click',()=>{const fit=b.closest('figure').querySelector('.diagram').classList.toggle('fit-width');b.setAttribute('aria-pressed',String(fit));b.textContent=fit?'Actual size':'Fit to width'}));
addEventListener('hashchange',()=>select(location.hash.slice(1)));select(location.hash.slice(1));
</script></html>'''
    top = [link("README.md", "Guide"), link("WORKFLOW_REVIEW.md", "Workflow assessment"),
           link("TRACEABILITY.md", "Traceability"), link("CHANGE_IMPACT.md", "Change exercise"),
           link("VALIDATION.json", "Published verification record")]
    content = (content.replace("__VERDICT__", escape(verdict)).replace("__COUNTS__", escape(counts))
               .replace("__TOP_LINKS__", "".join(top)).replace("__NAV__", "".join(nav))
               .replace("__PANELS__", "".join(panels)))
    (ROOT / "index.html").write_text(content, encoding="utf-8")
    print("Wrote", ROOT / "index.html")


if __name__ == "__main__":
    main()
