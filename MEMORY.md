# Memory

## 2026-10-04: chi_mixture_cap.py virtual `vh` roles are misaligned (do not reuse blindly)

- `virtual_post` in `experiments/chi_mixture_cap.py` appends the virtual slot for `vp` roles but PREPENDS it for `vh` roles (`vgeo = ((fresh_p, h),) + geo`), while the function always reads `assign[:t]` as the support statuses and `assign[t]` as the virtual. For `vh` this shifts the term law one slot against the geometry, so `vh` posteriors are not the intended same-line-partner values.
- The headline MIXTURE (d=2) results are unaffected: the winners were found and digit-exact-validated on support roles (Engine A's V2 pass), and the registered excesses equal the star-3M support posteriors. The `vh` entries only circulated as extra candidates in the V4 max scan and never won.
- `experiments/chi_mixture3.py` (MIXTURE-3) reimplements the virtual roles with the virtual always appended last; if you touch the cap script's role scan, mirror that fix or drop `vh` roles.
