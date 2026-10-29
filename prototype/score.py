"""Deterministic scoring + ranking from stored extractions.
No AI is called here: the same extraction file always gives the same ranking.
Usage: python score.py sample_extractions.json ../ranking.json
"""
import json, sys

WEIGHTS = {"experience": 30, "price": 25, "timeline": 15, "warranty": 15, "team": 15}
BUDGET, MAX_WEEKS = 260_000, 16
PANEL_FULL, WORK_FULL = 25, 12  # years that earn 100 points

def experience(n):
    if n is None: return None
    return 100 if n >= 12 else 80 if n >= 9 else 60 if n >= 6 else 30 if n >= 3 else 0

def mandatory(f):
    """Returns (status, reason). Unknown/ambiguous -> human review, never a silent pass."""
    if f.get("licence_held_by_bidder") is False:
        return "ineligible", "Fails mandatory licence criterion: bidder does not hold the licence itself (electrical work subcontracted, unnamed)."
    if f.get("licence_held_by_bidder") is None:
        return "flagged", "Licence not confirmed in the proposal."
    if not (f.get("wsib_clearance") and f.get("liability_insurance_5m")):
        return "flagged", "WSIB clearance or $5M insurance not confirmed."
    return "ok", ""

def main(src, out):
    data = json.load(open(src))
    elig = {k: v for k, v in data.items() if mandatory(v)[0] != "ineligible"}
    prices = [v["price_cad"] for v in elig.values() if v.get("price_cad") and v["price_cad"] <= BUDGET]
    weeks = [v["completion_weeks"] for v in elig.values()
             if v.get("completion_weeks") and v["completion_weeks"] <= MAX_WEEKS]
    results = []
    for k, f in data.items():
        status, reason = mandatory(f)
        if status == "ineligible":
            results.append(dict(proposal=k, rank=None, status="ineligible", score=None, reason=reason)); continue
        flags = []
        if f.get("injection_detected"): flags.append("hidden instruction aimed at automated reviewers (ignored; scored on real content only)")
        if f.get("completion_weeks") is None: flags.append("no completion schedule, so 16-week limit cannot be confirmed")
        if status == "flagged": flags.append(reason)
        s = {}
        s["experience"] = experience(f.get("installs_100kw_plus_last_5y"))
        p = f.get("price_cad")
        s["price"] = round(min(prices) / p * 100, 1) if p and p <= BUDGET else None
        w = f.get("completion_weeks")
        s["timeline"] = round(min(weeks) / w * 100, 1) if w and w <= MAX_WEEKS else None
        pw, ww = f.get("panel_warranty_years"), f.get("workmanship_warranty_years")
        s["warranty"] = None if pw is None or ww is None else round((min(pw / PANEL_FULL, 1) + min(ww / WORK_FULL, 1)) / 2 * 100, 1)
        s["team"] = 25 * sum(bool(f.get(x)) for x in ("named_project_lead", "crew_described", "safety_plan", "monitoring_plan"))
        total = sum((s[c] or 0) * wt / 100 for c, wt in WEIGHTS.items())  # missing = 0 points, flagged as provisional
        results.append(dict(proposal=k, status="flagged" if flags else "ranked", rank=None,
                            score=round(total + 1e-9, 1), criteria=s, flags=flags))
    ranked = sorted([r for r in results if r["status"] == "ranked"], key=lambda r: -r["score"])
    for i, r in enumerate(ranked, 1): r["rank"] = i
    for r in results:
        r["reason"] = r.get("reason") or (
            "; ".join(r["flags"]).capitalize() + ". Needs human review before ranking."
            if r.get("flags") else f"Passes mandatory criteria; weighted score {r['score']}.")
    order = {"ranked": 0, "flagged": 1, "ineligible": 2}
    results.sort(key=lambda r: (order[r["status"]], r["rank"] or 99, -(r["score"] or 0)))
    final = [{k: r[k] for k in ("proposal", "rank", "status", "score", "reason")} for r in results]
    json.dump(final, open(out, "w"), indent=1)
    for r in results: print(r["proposal"], r["status"], r["rank"], r["score"], r.get("criteria"))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
