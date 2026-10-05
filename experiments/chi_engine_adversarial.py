#!/usr/bin/env python3
"""chi_engine_adversarial.py -- ADVERSARIAL GATE for the inv3 completion engine.

Gate target: the degree-capped Buchberger completion engine in
experiments/chi_inv3_check.py (gb_complete / nf_full), whose closures back the
ideal-identity claim (I cap S_<=t = W_t) of docs/inv3.md.  The
reviewer-verified engine defects (docs/inv3.md downgrade block; GUIDANCE.md
problem 1) are:

  (a) Lemma TB (cls_cnt.md sect 3.2) is FALSE as stated; vacuous-hypothesis
      counterexample G = {x^2, xy+1} over F_2[x,y], t = 2: the identity is
      false there (1 in I cap S_<=2, 1 not in W_2).
  (b) the engine never examines pairs with lcm-degree > t
      (chi_inv3_check.py:412-415, 484-486), but such pairs' S-polynomials can
      have degree <= t; those residues are invisible to the run.
  (c) the verification pass can time out mid-scan and still report closure
      (chi_inv3_check.py:481, 495-496, 507).
  (d) the "independent configurations" are conjugate/overlapping (not a
      behavioral defect; the gate therefore probes one representative
      configuration, G / order A, and says so).

Verdict semantics: PASS = the engine behaves correctly (flags the false
identity, refuses closure on timeout, closes the true identities); FAIL = the
engine reports a wrong closure.  The overall verdict is EXPECTED to be FAIL
today, per the inv3 downgrade; the gate exists so that a REPAIRED engine can
be certified by re-running this same script unchanged.

Cases:

  case1  known-false identity: the real engine runs on G = {x^2, xy+1}, t = 2
         (generators injected through the engine's own module-level
         build_gens hook; a repaired engine should expose an explicit
         generator-set parameter instead).  Ground truth is established in
         this harness, not assumed: an UNCAPPED Groebner completion derives
         1 in I, and the exact echelon shows 1 not in W_2.  PASS iff the
         engine FLAGS the case (refuses closure); the recorded mode
         distinguishes FLAGS from known-false-closure-wrong.
  case2  lcm>t blind spot at the feasible 7x6 rectangle, t = 3, G / order A
         (a configuration the engine claims to close): every BASE generator
         pair with two disjoint degree-2 heads is enumerated; this includes
         exactly the star-row vs disjoint degree-2-row configuration named in
         the downgrade.  Each such S-polynomial is fully reduced by the
         engine's own division routine against the final G* (obtained from a
         mirror completion cross-checked against the engine run) and tested
         for span neutrality against the exact W_3 echelon.  A non-neutral
         residue is an explicit element of (I cap S_<=3) - W_3, i.e. an
         exotic the engine cannot see; finding one while the engine reports
         closure is FAIL.  All-neutral with full coverage is PASS, with the
         blind-spot counts recorded either way.
  case3  timeout honesty: the 7x6 t=3 completion (known from the registered
         inv3 run to need tens of seconds) is run under calibrated tight
         wall-clock caps.  PASS iff the engine refuses closure (INCOMPLETE)
         whenever the cap binds; FAIL if it reports closure within a cap that
         is strictly below the measured honest full-pass time of the same
         warm run (the verification scan then provably did not complete).
         This case is intrinsically timing-based; its calibration is printed.
  controls  known-TRUE: the t=2 completions at 5x4 and 7x6 (their conclusion
         is independently confirmed by the exact (6,3) dimension computation
         in chi_cls_cnt_check.py, per the downgrade's SURVIVES note) must
         still close.  Certification of a repaired engine = flag the false,
         refuse closure on timeout, still close the true.

Determinism: case1, case2 and the controls are fully deterministic (all
orderings derive from sort keys over int tuples; Python does not randomize
integer/tuple hashing).  Case 3 is calibrated timing by nature; its
calibration data are printed so the run is auditable.

Run:  cd /home/tomzx/pnp && python3 experiments/chi_engine_adversarial.py
      (--fast: shrinks the case-2 scan budget, skips the secondary 5x4 probe;
       --case1only: quick mechanical smoke of case 1)

Exit code: 0 = engine CERTIFIED by the adversarial gate (every gate case
PASS); 1 = engine NOT certified (the expected, documented outcome today).

No file is written; the gate prints its verdict table.
"""
import ast
import hashlib
import io
import os
import re
import sys
import time
from collections import Counter, defaultdict, deque
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import chi_inv3_check as chi  # the engine under test

T00 = time.time()
DEADLINE = T00 + 840.0                      # keep the whole gate inside ~15 min
FAST = "--fast" in sys.argv
CASE1ONLY = "--case1only" in sys.argv

RESULTS = []                                # (case, verdict, detail)
ORIG_BUILD_GENS = chi.build_gens


def remaining():
    return DEADLINE - time.time()


def record(case, verdict, detail=""):
    RESULTS.append((case, verdict, detail))
    print(f"[GATE-{verdict}] {case}" + (f"  {detail}" if detail else ""), flush=True)


# ---------------------------------------------------------------------------
# engine-run helper (captures the engine's own prints for parsing)
# ---------------------------------------------------------------------------

def run_engine(np_, nh, t, variant, kind, wt, midx, tag, time_cap):
    buf = io.StringIO()
    t0 = time.time()
    with redirect_stdout(buf):
        ok = chi.gb_complete(np_, nh, t, variant, kind, wt, midx, tag,
                             time_cap=time_cap, scope="diagnostic")
    return ok, time.time() - t0, buf.getvalue()


def status_word(out):
    if "completion closed" in out:
        return "closed"
    if "EXOTIC RELATION" in out:
        return "EXOTIC"
    if "INCOMPLETE" in out:
        return "INCOMPLETE"
    return "?"


def parse_trace(out):
    m = re.search(r"(\d+)\+(\d+) gens \((\{[^}]*\}) by degree\), "
                  r"(\d+) pairs processed, (\d+) pass\(es\)", out)
    if not m:
        return None
    return dict(base=int(m.group(1)), added=int(m.group(2)),
                degs=dict(ast.literal_eval(m.group(3))),
                processed=int(m.group(4)), passes=int(m.group(5)),
                status=status_word(out))


def build_echelon(np_, nh, cap):
    monos = chi.rect_monomials(np_, nh, cap)
    midx = {m: k for k, m in enumerate(monos)}
    piv = chi.echelon(chi.dedupe(chi.rect_rows(np_, nh, cap, monos, midx)))
    return piv, midx


# ---------------------------------------------------------------------------
# case 1: the Lemma TB counterexample, with harness-established ground truth
# ---------------------------------------------------------------------------

def uncapped_gb(gens, key, max_add=200):
    """UNCAPPED Buchberger completion (ground-truth instrument; the ideal
    (x^2, xy+1) contains 1, which this loop derives in two additions)."""
    gens = [frozenset(g) for g in gens]
    heads = [max(g, key=key) for g in gens]
    by_head = defaultdict(list)
    for i, h in enumerate(heads):
        by_head[h].append(i)
    todo = deque((i, j) for i in range(len(gens))
                 for j in range(i + 1, len(gens)))
    n = 0
    while todo and n < max_add:
        i, j = todo.popleft()
        hi, hj = heads[i], heads[j]
        L = chi.mlcm(hi, hj)
        S = chi.padd(chi.pmul(gens[i], {chi.mquo(L, hi)}),
                     chi.pmul(gens[j], {chi.mquo(L, hj)}))
        if not S:
            continue
        R = chi.nf_full(S, gens, heads, by_head, key)
        if R:
            gens.append(R)
            heads.append(max(R, key=key))
            by_head[heads[-1]].append(len(gens) - 1)
            nn = len(gens) - 1
            for k in range(nn):
                todo.append((k, nn))
            n += 1
            if () in R:
                break
    return gens


def case1():
    np_, nh, t = 1, 2, 2                 # cells: 0 = x, 1 = y
    G1 = [("x2", frozenset({(0, 0)})),
          ("xy1", frozenset({(0, 1), ()}))]
    monos = chi.rect_monomials(np_, nh, t)
    midx = {m: k for k, m in enumerate(monos)}
    rows = []                            # W_2 = span{m*h : deg(mh) <= 2}
    for _, g in G1:
        dg = max(len(u) for u in g)
        for m in monos:
            if len(m) + dg <= t:
                vv = 0
                for u in g:
                    vv |= 1 << midx[tuple(sorted(m + u))]
                rows.append(vv)
    wt = chi.echelon(chi.dedupe(rows))
    one_in_W = chi.in_span(1, wt)        # 1 = e_( ) ; exact echelon decision
    key = chi.order_key("A", np_, nh)
    gb = uncapped_gb([g for _, g in G1], key)
    one_in_I = any(() in g for g in gb)  # uncapped completion derives 1
    if not (one_in_I and not one_in_W):
        record("case1 ground truth self-check", "FAIL",
               "harness ground truth broken: the TB counterexample does not "
               f"falsify the identity (1 in I: {one_in_I}, 1 in W_2: {one_in_W})")
        return None
    chi.build_gens = lambda a, b, c: list(G1)
    try:
        ok, el, out = run_engine(np_, nh, t, "G", "A", wt, midx,
                                 "TB-counterexample", 60.0)
    finally:
        chi.build_gens = ORIG_BUILD_GENS
    tr = parse_trace(out)
    mode = "FLAGS (refuses closure)" if not ok else "known-false-closure-wrong"
    verdict = "PASS" if not ok else "FAIL"
    record("case1 TB counterexample G={x^2,xy+1}, t=2 (identity FALSE)",
           verdict,
           f"mode: {mode}; ground truth: 1 in I = {one_in_I} (uncapped GB), "
           f"1 in W_2 = {one_in_W} (echelon); engine closure claim: "
           f"ok={ok}, trace {tr}, {el:.1f}s")
    return ok


# ---------------------------------------------------------------------------
# known-TRUE controls
# ---------------------------------------------------------------------------

def known_true(np_, nh):
    t = 2
    monos = chi.rect_monomials(np_, nh, t)
    midx = {m: k for k, m in enumerate(monos)}
    wt = chi.echelon(chi.dedupe(chi.rect_rows(np_, nh, t, monos, midx)))
    ok, el, out = run_engine(np_, nh, t, "G", "A", wt, midx,
                             f"{np_}x{nh}", 180.0)
    record(f"known-TRUE control: t=2 closure at {np_}x{nh} must close",
           "PASS" if ok else "FAIL",
           f"engine closure claim: ok={ok} ({status_word(out)}), {el:.1f}s")


# ---------------------------------------------------------------------------
# case 3: timeout honesty
# ---------------------------------------------------------------------------

def case3(piv63, midx63):
    args = (7, 6, 3, "G", "A", piv63, midx63, "7x6")
    okA, tA, outA = run_engine(*args, time_cap=420.0)     # warm-up
    okB, tB, outB = run_engine(*args, time_cap=420.0)     # honest reference
    trB = parse_trace(outB)
    verdict = None
    for f in (0.75, 0.60, 0.85):
        cap = max(1.0, f * tB)
        okC, tC, outC = run_engine(*args, time_cap=cap)
        if not okC:
            verdict = ("PASS",
                       f"cap {cap:.1f}s bound the run: engine refused closure "
                       f"({status_word(outC)}, {tC:.1f}s)")
            break
        if tC <= cap + 1.0 and tB >= 1.25 * (cap + 1.0):
            verdict = ("FAIL",
                       f"closure reported at {tC:.1f}s <= cap {cap:.1f}s, but "
                       f"the same warm honest run needs {tB:.1f}s: the "
                       f"verification scan provably did not complete (defect "
                       f"(c): chi_inv3_check.py:481,495-496,507)")
            break
        # cap overshot before the engine decided: try the next rung
    if verdict is None:
        verdict = ("INCONCLUSIVE",
                   f"no cap cleanly bound the scan (T_ref={tB:.1f}s)")
    calib = (f"calibration: warm-up {tA:.1f}s (ok={okA}), honest reference "
             f"T_ref={tB:.1f}s (ok={okB}, trace {trB})")
    record("case3 timeout honesty at 7x6 t=3 under tight caps",
           verdict[0], verdict[1] + "; " + calib)
    return okB, trB


# ---------------------------------------------------------------------------
# case 2: the lcm>t blind spot (mirror completion + hidden-pair scan)
# ---------------------------------------------------------------------------

def shadow_complete(base_named, np_, nh, t, kind, wt_piv, midx,
                    time_cap=420.0, max_added=5000):
    """Verbatim mirror of chi_inv3_check.gb_complete (lines 377-527) with the
    base generator set passed in explicitly and the final state returned.
    cross_check below compares it against the engine run; any divergence
    invalidates the hidden-pair scan (the scan only acts on a certified G*)."""
    t0 = time.time()
    key = chi.order_key(kind, np_, nh)
    gens = [g for _, g in base_named]
    heads = [max(g, key=key) for g in gens]
    by_head = defaultdict(list)
    for i, h in enumerate(heads):
        by_head[h].append(i)
    base = len(gens)

    def vec_of(p):
        vv = 0
        for m in p:
            vv |= 1 << midx[m]
        return vv

    shift_cache = {}

    def verify_neutral(R):
        if not chi.in_span(vec_of(R), wt_piv):
            return "R not in W_t"
        dg = max(len(m) for m in R)
        sms = shift_cache.get(dg)
        if sms is None:
            sms = [m for m in midx if len(m) <= t - dg]
            shift_cache[dg] = sms
        for m in sms:
            sh = frozenset(tuple(sorted(m + u)) for u in R)
            if not chi.in_span(vec_of(sh), wt_piv):
                return f"shift {m} not in W_t"
        return None

    def lcm_ok(i, j):
        hi, hj = heads[i], heads[j]
        if len(set(hi) | set(hj)) > t:
            return False
        return len(chi.mlcm(hi, hj)) <= t

    queue = deque()
    inq = set()
    for i in range(base):
        for j in range(i + 1, base):
            if lcm_ok(i, j):
                queue.append((i, j))
                inq.add((i, j))

    exotic = None
    added = 0
    added_degs = []
    processed = 0
    passes = 0

    def process_queue():
        nonlocal processed, added, exotic
        while queue:
            if time.time() - t0 > time_cap or added > max_added:
                return False
            i, j = queue.popleft()
            inq.discard((i, j))
            processed += 1
            hi, hj = heads[i], heads[j]
            L = chi.mlcm(hi, hj)
            if len(L) > t:
                continue
            S = chi.padd(chi.pmul(gens[i], {chi.mquo(L, hi)}),
                         chi.pmul(gens[j], {chi.mquo(L, hj)}))
            if not S:
                continue
            R = chi.nf_full(S, gens, heads, by_head, key)
            if R:
                if add_if_neutral(R, f"pair ({i},{j})") is False:
                    return False
        return True

    def add_if_neutral(R, src):
        nonlocal added, exotic
        why = verify_neutral(R)
        if why is not None:
            exotic = (src, sorted(R), why)
            return False
        gens.append(R)
        heads.append(max(R, key=key))
        by_head[heads[-1]].append(len(gens) - 1)
        n = len(gens) - 1
        for k in range(n):
            if lcm_ok(k, n) and (k, n) not in inq:
                queue.append((k, n))
                inq.add((k, n))
        added += 1
        added_degs.append(max(len(m) for m in R))
        return True

    while True:
        passes += 1
        if not process_queue():
            break
        bad = []
        n = len(gens)
        for i in range(n):
            if exotic is not None or time.time() - t0 > time_cap:
                break
            hi = heads[i]
            shi = set(hi)
            for j in range(i + 1, n):
                if len(shi | set(heads[j])) > t:
                    continue
                if len(chi.mlcm(hi, heads[j])) > t:
                    continue
                L = chi.mlcm(hi, heads[j])
                S = chi.padd(chi.pmul(gens[i], {chi.mquo(L, hi)}),
                             chi.pmul(gens[j], {chi.mquo(L, heads[j])}))
                if not S:
                    continue
                R = chi.nf_full(S, gens, heads, by_head, key)
                if R:
                    bad.append((i, j, R))
        if exotic is not None:
            break
        if not bad:
            break
        for (i, j, R) in bad:
            if add_if_neutral(R, f"verify ({i},{j})") is False:
                break
        if exotic is not None or passes >= 6:
            break
        for i in range(base, len(gens)):
            for j in range(i):
                if lcm_ok(j, i) and (j, i) not in inq:
                    queue.append((j, i))
                    inq.add((j, i))

    ok = (exotic is None) and (not queue)
    return dict(ok=ok, gens=gens, heads=heads, by_head=by_head, base=base,
                added=added, added_degs=added_degs, processed=processed,
                passes=passes, exotic=exotic, elapsed=time.time() - t0)


def cross_check(sh, trace, ok_engine):
    if trace is None:
        return False, "engine trace unparseable"
    same = (sh["base"] == trace["base"] and sh["added"] == trace["added"]
            and dict(sorted(Counter(sh["added_degs"]).items())) == trace["degs"]
            and sh["processed"] == trace["processed"]
            and sh["passes"] == trace["passes"]
            and sh["ok"] == ok_engine)
    desc = (f"shadow: {sh['base']}+{sh['added']} gens "
            f"({dict(sorted(Counter(sh['added_degs']).items()))} by degree), "
            f"{sh['processed']} pairs, {sh['passes']} pass(es), ok={sh['ok']}; "
            f"engine: {trace}")
    return same, desc


def family(name):
    return re.match(r"[A-Za-z']+", name).group(0)


def neutrality(R, t, wt_piv, midx, sms_cache):
    """Mirror of the engine's verify_neutral criterion: R in W_t AND every
    <=t shift of R in W_t.  Exact decisions against the base-generator W_t."""
    vv = 0
    for m in R:
        vv |= 1 << midx[m]
    if not chi.in_span(vv, wt_piv):
        return "R not in W_t"
    dg = max(len(m) for m in R)
    sms = sms_cache.get(dg)
    if sms is None:
        sms = [m for m in midx if len(m) <= t - dg]
        sms_cache[dg] = sms
    for m in sms:
        vv = 0
        for u in R:
            vv |= 1 << midx[tuple(sorted(m + u))]
        if not chi.in_span(vv, wt_piv):
            return f"shift {m} not in W_t"
    return None


def hidden_scan(np_, nh, t, variant, kind, wt_piv, midx, shadow, budget):
    """Enumerate every BASE pair whose two heads are disjoint degree-2
    monomials (lcm-degree 4 > t: exactly the class the engine's lcm_ok and
    verification pass skip).  Includes the star-row vs disjoint degree-2-row
    configuration named in the downgrade.  Each S-polynomial is fully reduced
    by the engine's own nf_full against the final G*; in-cap residues are
    deduplicated and tested for span neutrality against W_t."""
    key = chi.order_key(kind, np_, nh)
    gens, heads = shadow["gens"], shadow["heads"]
    by_head, base = shadow["by_head"], shadow["base"]
    fams = [family(n) for n, _ in chi.build_gens(np_, nh, variant)]
    per_class = defaultdict(list)
    for i in range(base):
        if len(heads[i]) != 2:
            continue
        hi = set(heads[i])
        for j in range(i + 1, base):
            if len(heads[j]) != 2:
                continue
            if hi & set(heads[j]):
                continue                     # overlap => lcm <= 3 => examined
            per_class[tuple(sorted((fams[i], fams[j])))].append((i, j))
    cls_total = {c: len(v) for c, v in per_class.items()}
    order = []                               # round-robin: coverage spans classes
    idx = 0
    while any(idx < len(v) for _, v in sorted(per_class.items())):
        for _, v in sorted(per_class.items()):
            if idx < len(v):
                order.append(v[idx])
        idx += 1
    t0 = time.time()
    examined = 0
    cls_exam = Counter()
    n_S0 = 0
    n_over = 0
    over_cls = Counter()
    residues = {}                            # distinct in-cap residue -> source
    complete = True
    for (i, j) in order:
        examined += 1
        cls_exam[tuple(sorted((fams[i], fams[j])))] += 1
        if examined % 128 == 0 and time.time() - t0 > budget:
            complete = False
            break
        hi, hj = heads[i], heads[j]
        L = chi.mlcm(hi, hj)
        S = chi.padd(chi.pmul(gens[i], {chi.mquo(L, hi)}),
                     chi.pmul(gens[j], {chi.mquo(L, hj)}))
        if not S:
            n_S0 += 1
            continue
        R = chi.nf_full(S, gens, heads, by_head, key)
        if not R:
            n_S0 += 1
            continue
        if max(len(m) for m in R) > t:
            n_over += 1
            over_cls[tuple(sorted((fams[i], fams[j])))] += 1
            continue
        if R not in residues:
            residues[R] = (i, j)
    # sound shortcut: a residue that IS a base row m*g (deg <= t) has all its
    # <=t shifts equal to (m'*m)*g, again rows of W_t: neutral by construction
    rowset = set()
    for _, g in chi.build_gens(np_, nh, variant):
        dg = max(len(u) for u in g)
        for m in midx:
            if len(m) + dg <= t:
                rowset.add(chi.pmul({m}, g))
    sms_cache = {}
    n_dict = 0
    checked = 0
    exotic = None
    neut_complete = True
    for R in sorted(residues, key=sorted):
        if R in rowset:
            n_dict += 1
            continue
        checked += 1
        if time.time() - t0 > budget:
            neut_complete = False
            break
        why = neutrality(R, t, wt_piv, midx, sms_cache)
        if why is not None:
            i, j = residues[R]
            names = [n for n, _ in chi.build_gens(np_, nh, variant)]
            exotic = dict(source=(names[i], names[j]), residue=sorted(R), why=why)
            break
    return dict(n_hidden=len(order), examined=examined, complete=complete,
                n_S0=n_S0, n_over=n_over, over_cls=dict(over_cls),
                n_residues=len(residues),
                n_dict=n_dict, n_echelon=checked, exotic=exotic,
                neut_complete=neut_complete, cls_total=cls_total,
                cls_exam=dict(cls_exam), elapsed=time.time() - t0)


def neutrality_selfcheck(np_, nh, t, variant, kind, wt_piv, midx, shadow):
    """Validate the membership machinery on both known paths before trusting
    the scan.  Member path: a base degree-2 row is a spanning row of W_t, so
    exact in_span must accept it.  Non-member path: if the mirror completion
    stopped on an exotic, its residue must FAIL neutrality (that also
    exercises the shift checks); otherwise use the recorded corpus fact
    e0 not in V (chi_inv3_check.py part D)."""
    g0 = None
    for _, g in chi.build_gens(np_, nh, variant):
        if max(len(u) for u in g) == 2:
            g0 = g
            break
    vv = 0
    for m in g0:
        vv |= 1 << midx[m]
    ok_mem = chi.in_span(vv, wt_piv)
    if shadow["exotic"] is not None:
        bad = frozenset(tuple(m) for m in shadow["exotic"][1])
        ok_non = neutrality(bad, t, wt_piv, midx, {}) is not None
    else:
        ok_non = not chi.in_span(1, wt_piv)
    return bool(ok_mem and ok_non), (bool(ok_mem), bool(ok_non))


def case2(piv63, midx63, okB, trB):
    np_, nh, t = 7, 6, 3
    variant, kind = "G", "A"
    base_named = chi.build_gens(np_, nh, variant)
    shadow = shadow_complete(base_named, np_, nh, t, kind, piv63, midx63)
    same, desc = cross_check(shadow, trB, okB)
    if not same:
        record("case2 lcm>t blind spot at 7x6, t=3 (G/order A)", "INCONCLUSIVE",
               "mirror completion does not match the engine run; hidden-pair "
               f"scan not certified. {desc}")
        return
    budget = max(60.0, min(420.0, remaining() - 180.0))
    sc_ok, sc_why = neutrality_selfcheck(np_, nh, t, variant, kind,
                                         piv63, midx63, shadow)
    if not sc_ok:
        record("case2 lcm>t blind spot at 7x6, t=3 (G/order A)", "INCONCLUSIVE",
               f"neutrality self-check failed {sc_why}; scan results void. "
               f"cross-check: {desc}")
        return
    scan = hidden_scan(np_, nh, t, variant, kind, piv63, midx63, shadow, budget)
    ex = scan["exotic"]
    div_word = "complete" if scan["complete"] else f"INCOMPLETE (budget {budget:.0f}s)"
    neut_word = "complete" if scan["neut_complete"] else "INCOMPLETE"
    coverage = (f"hidden pairs (disjoint degree-2 heads, lcm-degree 4): "
                f"{scan['n_hidden']}, examined {scan['examined']} "
                f"({div_word}); S=0 or in-cap reduction to 0: {scan['n_S0']}, "
                f"residue degree >t: {scan['n_over']} "
                f"(classes {scan['over_cls']}); distinct in-cap residues: "
                f"{scan['n_residues']} (row-shortcut {scan['n_dict']}, "
                f"echelon-checked {scan['n_echelon']}, neutrality {neut_word})")
    if ex is not None:
        witness = (f"EXOTIC from hidden pair {ex['source']}: why={ex['why']}, "
                   f"residue={ex['residue']}")
        if okB:
            record("case2 lcm>t blind spot at 7x6, t=3 (G/order A)", "FAIL",
                   f"engine reported closure (ok=True) while a hidden lcm>t "
                   f"pair leaves an element of (I cap S_<=3) - W_3. {witness}. "
                   f"{coverage}. cross-check: {desc}")
        else:
            record("case2 lcm>t blind spot at 7x6, t=3 (G/order A)", "PASS",
                   f"engine refused closure, hidden exotic confirmed: {witness}. "
                   f"{coverage}. cross-check: {desc}")
        return
    if not (scan["complete"] and scan["neut_complete"]):
        record("case2 lcm>t blind spot at 7x6, t=3 (G/order A)", "INCONCLUSIVE",
               f"scan budget exhausted before a verdict; blind spot is "
               f"structural (engine skips all these pairs) but the exotic "
               f"search is incomplete. engine closure claim ok={okB}. "
               f"{coverage}. cross-check: {desc}")
        return
    if scan["n_residues"] == 0 and scan["n_over"] > 0:
        finding = (f"no in-cap residue exists at this probe: none of the "
                   f"{scan['n_hidden']} hidden S-polynomials the engine never "
                   f"examined reduces to a degree<=3 nonzero residue "
                   f"({scan['n_over']} leave degree->3 residues, recorded and "
                   f"out of the (star)_3 scope), so the blind spot does not "
                   f"bite here")
    else:
        finding = (f"all {scan['n_residues']} distinct in-cap hidden residues "
                   f"are W_3-neutral")
    record("case2 lcm>t blind spot at 7x6, t=3 (G/order A)", "PASS",
           f"{finding}; the engine's closure (ok={okB}) is unrefuted at this "
           f"probe but NOT certified by its own logic (all {scan['n_hidden']} "
           f"hidden pairs are skipped by chi_inv3_check.py:412-415,484-486, "
           f"and the closure claim rests on the false Lemma TB). {coverage}. "
           f"cross-check: {desc}")


def probe54():
    """Secondary informational probe at 5x4, t=3: the rectangle where the
    identity is FALSE (inv3 sect 3.4).  Do hidden lcm>t pairs also exhibit
    exotics there?  Not a gate verdict (the engine already refuses there)."""
    np_, nh, t = 5, 4, 3
    variant, kind = "G", "A"
    wt, midx = build_echelon(np_, nh, t)
    okE, tE, outE = run_engine(np_, nh, t, variant, kind, wt, midx, "5x4", 120.0)
    base_named = chi.build_gens(np_, nh, variant)
    shadow = shadow_complete(base_named, np_, nh, t, kind, wt, midx)
    same, desc = cross_check(shadow, parse_trace(outE), okE)
    sc_ok, sc_why = neutrality_selfcheck(np_, nh, t, variant, kind, wt, midx, shadow)
    if not sc_ok:
        record("note-5x4 informational probe (identity FALSE there; not a gate case)",
               "NOTE", f"neutrality self-check failed {sc_why}; cross-check ok={same}")
        return
    scan = hidden_scan(np_, nh, t, variant, kind, wt, midx, shadow,
                       budget=max(45.0, min(150.0, remaining() - 60.0)))
    ex = scan["exotic"]
    cov = (f"hidden scan: {scan['n_hidden']} hidden pairs, examined "
           f"{scan['examined']} (coverage "
           f"{'full' if scan['complete'] and scan['neut_complete'] else 'partial'}), "
           f"S=0/zero {scan['n_S0']}, over-cap {scan['n_over']}, in-cap "
           f"residues {scan['n_residues']}")
    if ex is not None:
        exmsg = (f"EXOTIC via the blind spot from hidden pair {ex['source']}: "
                 f"{ex['why']}, residue={ex['residue']}")
    else:
        exmsg = "no exotic via the blind spot at this rectangle"
    record("note-5x4 informational probe (identity FALSE there; not a gate case)",
           "NOTE",
           f"engine refusal at 5x4 t=3: ok={okE} ({status_word(outE)}, "
           f"{tE:.1f}s); {exmsg}; {cov}; cross-check ok={same}")


# ---------------------------------------------------------------------------
# verdict table
# ---------------------------------------------------------------------------

def final_table():
    print("\n== ADVERSARIAL GATE VERDICT TABLE ==", flush=True)
    gate_rows = [r for r in RESULTS
                 if r[0].startswith(("case1", "case2 ", "case3", "known-TRUE"))]
    for case, verdict, detail in RESULTS:
        print(f"  {verdict:>12} | {case}")
        if detail:
            print(f"               |   {detail}")
    overall = ("PASS" if gate_rows and all(v == "PASS" for _, v, _ in gate_rows)
               else "FAIL")
    print(f"  {'OVERALL':>12} | {overall}")
    if overall == "PASS":
        print("  ENGINE CERTIFIED by the adversarial gate "
              "(flags the known-false, refuses closure on timeout, "
              "still closes the known-TRUE).")
    else:
        print("  ENGINE NOT CERTIFIED (expected today per the docs/inv3.md "
              "downgrade; re-run this gate unchanged after repair: "
              "certification = every gate case PASS).")
    print(f"== total {time.time()-T00:.1f}s ==", flush=True)
    return 0 if overall == "PASS" else 1


# ---------------------------------------------------------------------------

def main():
    sha = hashlib.sha256(open(chi.__file__, "rb").read()).hexdigest()[:16]
    print("== chi_engine_adversarial: adversarial gate for the inv3 "
          "completion engine ==", flush=True)
    print(f"engine under test: experiments/chi_inv3_check.py (sha256 {sha})")
    print(f"--fast={FAST}  case2 scan budget set at run time; deadline guard "
          f"{DEADLINE - T00:.0f}s")
    print("registered run: cd /home/tomzx/pnp && python3 "
          "experiments/chi_engine_adversarial.py", flush=True)

    case1()
    if CASE1ONLY:
        return final_table()

    known_true(5, 4)
    known_true(7, 6)

    piv63, midx63 = build_echelon(7, 6, 3)
    okB, trB = case3(piv63, midx63)
    case2(piv63, midx63, okB, trB)

    if not FAST and remaining() > 240.0:
        probe54()
    elif not FAST:
        record("note-5x4 informational probe (identity FALSE there; not a gate case)",
               "NOTE", "skipped: global time guard")
    return final_table()


if __name__ == "__main__":
    sys.exit(main())
