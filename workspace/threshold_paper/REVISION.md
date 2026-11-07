<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Upper-bound revision

The paper now includes the strongest general exact construction from the research thread and the improved average-case upper bounds, with self-contained proofs and raw-gate accounting.

- Exact: $(5/16+o(1))n^2$ total gates at balance. The finite bottom-gate formula is stated explicitly; exact balance also gives the negative $n\log n/4$ correction up to $O(n)$.
- Approximation: $O(n^{3/2}\sqrt{\log(1/\delta)})$ gates for agreement $1-\delta$, and $O(\varepsilon^2 n^{3/2}\sqrt{\log(1/\varepsilon)})$ gates over the stated small-advantage regime. The proof fixes masks nonuniformly; it makes no efficient uniform mask-selection claim.
- Formalization: distinguishes the two new hand proofs from merged Lean proofs of the earlier bounds. PRs 2377, 2813 and 2814 are merged; 2816 is open as checked on 7 November 2026.

The earlier simpler quadratic construction remains as an introduction. The unrelated moduli proof sketch was removed to keep the revision focused. Finite SMT records, experimental coefficient languages, failed approaches, and the unreviewed lower-bound-range extension remain in the research archive rather than the paper. A small positive-part correction makes the sign-coherent appendix's entropy bound valid in trivial parameter regimes.

Validation:

```sh
python3 verify_upper_updates.py
tectonic paper.tex
```

`upper_update_checks.json` records 58,264 exhaustive table/block-count cases for the new raw gate construction, larger spot checks, and independent exact cross-moment checks. Block-count enumeration is complete here because every exact-construction gate and direct coefficient is uniform inside its block. The mathematical proofs establish the all-size statements; finite checks are guardrails.

The revised PDF is 19 pages (previously 18). All labels resolve, no overfull boxes or undefined references were reported, and the new result pages were visually inspected. The source and PDF are preserved together in the private continuation archive.
