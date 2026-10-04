# Theorem dependency map: the p=2 program of arXiv:2609.35927 (v2, 2026-10-04)

Three focused diagrams: (1) foundations and the coin-channel layer, (2) the
true-pipeline theory, (3) the open gaps and the conditional route. Green = proved
and computation-verified; red dashed = retractions with provenance; yellow dashed =
open gaps; the route to the objective runs through Theorem 6.1's err-form assembly
(chi_transfer.md Theorem 4), since the printed chi-hypothesis (3) is false as
printed. Full retraction provenance in LOG.md; references in bibliography.md.

## 1. Foundations and the coin-channel layer

```mermaid
flowchart TD
    KRA["Krajicek pipeline Omega(n,d) at p=2<br/>arXiv:2609.35927, Def 4.3"]:::ext
    KERNEL["ONE kernel: V(n,d)^rho = V(2d,d)<br/>outer = canonical reading"]:::proved
    CL["Channel law, kernel-true:<br/>row-incomplete fair coins; full free rows<br/>parity-locked (XOR=1); Q_i = 0 on all pigeons"]:::proved
    LIN["Lemma 1: F_2 linearity<br/>ans(g) = a + XOR of variable answers"]:::proved
    REL["Lemma REL: coin channel = true channel<br/>below per-row cost Theta(n)"]:::proved
    L3["Lemma 3: counting certificates<br/>killed rows and columns show exactly one 1"]:::proved
    LEMC["Lemma C = Theorem 1: ADJACENCY certificates<br/>two adjacent 1s give certainty"]:::proved
    PRODAC["Props A, C: variable-class caps"]:::proved
    LEMB1["Lemma B.1: depletion bound<br/>quantifier repaired; 35/35 exact grid"]:::proved
    THB["Theorem B: adaptive single-variable cap<br/>success at most q + budget slack"]:::proved
    ANDNL["AND-no-lift: single-pass posterior = q<br/>q_and = 0.2763 at (32,2), measured"]:::proved
    THF["Theorem F: exact COIN-channel floor<br/>err* = 2^-Theta(d^2), counting tree"]:::proved
    THT["Theorem T, literal:<br/>err = 5 x 2^-(2d+1) at d = 2<br/>coin-model only"]:::proved
    ART["RETRACTED: Theorem T 'exact law'<br/>1 - 2^-(2d+1) (simulator artifact)"]:::retr

    KRA --> KERNEL
    KERNEL --> CL
    CL --> REL
    LIN --> REL
    CL --> L3
    CL --> LEMC
    REL --> PRODAC
    REL --> LEMB1
    REL --> ANDNL
    REL --> THT
    PRODAC --> THB
    LEMB1 --> THB
    LIN --> THF
    L3 --> THF
    ART -.->|supersedes| THT

    classDef proved fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20
    classDef retr fill:#ffebee,stroke:#b71c1c,color:#b71c1c,stroke-dasharray: 5 5
    classDef ext fill:#e3f2fd,stroke:#0d47a1,color:#0d47a1
```

## 2. The true-pipeline theory (post-correction)

```mermaid
flowchart TD
    CLR["Channel law (kernel-true)<br/>see diagram 1"]:::ext
    TH2["Theorem 2: one-row posteriors<br/>parity-suppressed below q"]:::proved
    THB["Theorem B (diagram 1)"]:::proved
    LEMC["Lemma C (diagram 1)"]:::proved
    L3["Lemma 3 (diagram 1)"]:::proved
    TH3["Theorem 3: BUDGETED CAP, full degree-<=2<br/>success at most q + P_adj + P_K + o(1)"]:::proved
    COR31["Cor 3.1: chi-hypothesis ALIVE<br/>whenever d^2 log k = o(n)"]:::proved
    S8["Sec 8: budgeted boundary<br/>err*(d, d log k) = k^-Theta(d^2/n)"]:::proved
    TH4B["Theorem 4b: K_j column-parity tree<br/>strongest budgeted attacker (0.9692 at (32,2))"]:::proved
    TH5["Theorem 5: full-scan success EXACTLY 1<br/>on the true pipeline"]:::proved
    THF["Theorem F (diagram 1): coin-channel floor"]:::proved
    OLDFLOOR["RETRACTED: 2^-Theta(d) floor conjecture"]:::retr
    PROPD["RETRACTED: Prop D as stated<br/>rc counterexample 0.9067 vs 0.625"]:::retr
    PARITY4["CORRECTED: parity-locked floor<br/>terminates at 0, not ~4x"]:::retr

    CLR --> TH2
    CLR --> TH4B
    CLR --> TH5
    THB --> TH3
    LEMC --> TH3
    L3 --> TH3
    TH2 --> TH3
    TH3 --> COR31
    TH3 --> S8
    TH4B --> S8
    TH5 -.->|requalifies as coin-only| THF
    OLDFLOOR -.->|refuted by| THF
    PROPD -.->|surviving form feeds| TH3
    PARITY4 -.-> TH5

    classDef proved fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20
    classDef retr fill:#ffebee,stroke:#b71c1c,color:#b71c1c,stroke-dasharray: 5 5
    classDef ext fill:#e3f2fd,stroke:#0d47a1,color:#0d47a1
```

## 3. Open gaps and the conditional route (updated for chi-transfer)

```mermaid
flowchart TD
    COR31["Cor 3.1: degree-2 slice proved"]:::proved
    GAPD3["GAP A: degree >= 4 extension<br/>degrees 2 AND 3 proved (Theorem 3',<br/>deg3_theory.md: same d^2 ~ n boundary;<br/>wedge + Z certificates; star sum rules)"]:::gap
    GAPB["GAP B: RESOLVED (chi_transfer.md)<br/>printed Theorem 6.1(3) is FALSE as printed<br/>(trivial row-sum tree: err >= 1/2 but<br/>chi = (1-f) p^-e' = k^-Theta(d));<br/>transfer reversed: (P3) <= (P2)"]:::resolved
    MIX["GAP B': Theorem 3's query classes are a<br/>proper subset of the printed degree-2 class<br/>(F_2 mixtures; likely shallow repair)"]:::gap
    GAPLM["GAP C: Lemma M (O5) degree-2<br/>monomial semantics transfer"]:::gap
    GAPJDP["GAP D: de-modularize JDP steps"]:::gap
    GAPCST["GAP E: exact exponent constants<br/>cap ~0.32 vs witness 0.06 at (128,2)"]:::gap
    GAPO6["GAP F: O6 odd-p analogue"]:::gap
    ROUTE["The err-form route (chi_transfer.md Thm 4):<br/>Def 3.1 + Lemma 4.4 + Thms 2.2/3.2/3.3<br/>applied to the BUDGETED ERR-FLOOR (O2)<br/>- the printed (3) is replaced by this"]:::cond
    OBJ["Super-poly AC0[2]-Frege PHP bounds<br/>- a rung toward P != NP<br/>(Cook-Reckhow: not the separation itself)"]:::goal

    COR31 --> GAPD3
    COR31 --> ROUTE
    MIX --> ROUTE
    TH3X["Theorem 3, full coverage"]:::proved
    GAPLM --> TH3X
    GAPJDP --> TH3X
    TH3X --> ROUTE
    GAPCST --> ROUTE
    GAPB -.->|killed the printed route| ROUTE
    GAPD3 --> ROUTE
    ROUTE -->|"if O2 proved at all degrees"| OBJ
    GAPO6 -.->|second front| OBJ

    classDef proved fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20
    classDef gap fill:#fff8e1,stroke:#f57f17,color:#795548,stroke-dasharray: 5 5
    classDef resolved fill:#e0f2f1,stroke:#00695c,color:#00695c
    classDef cond fill:#fff3e0,stroke:#e65100,color:#e65100
    classDef goal fill:#f3e5f5,stroke:#4a148c,color:#4a148c,stroke-width:3px
```

## Notes

- The retraction chain, end to end: Theorem T's artifact law -> Prop D -> the
  2^{-Theta(d)} floor -> the ~4x parity-lock expectation -> the printed (3).
  Each is kept in LOG.md with full provenance; the four theorem-level ghosts
  appear in diagrams 1-2, the printed-(3) kill in diagram 3.
- GAP B resolved NEGATIVELY for the printed route and POSITIVELY for the corpus:
  the printed (3) is unprovable by any err-cap (reversed transfer) and false as
  printed; the err-form assembly is both correct and exactly what O2 targets.
- GAP A (degree >= 3) is the single remaining load-bearing gap: with it, the
  err-form route's premise is a proved theorem in the program's polylog regime.
- Validation: mmdc unavailable (disk 437 MB free at write time); each block
  passed the structural check (declared endpoints, quote balance, subgraph
  matching). `flowchart` renders on GitHub; no front matter is used inside the
  fences (some renderers reject YAML in fenced blocks).
