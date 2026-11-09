<!-- Copyright (c) 2026 Christian Reitwiessner. All rights reserved. -->
Authors: Christian Reitwiessner

# Research state

Latest research snapshot: [9 November 2026 update](UPDATE_2026-11-09.md) — explainer, coherence results, and explicitly incomplete Astra investigations.


## 1. Common definitions and conventions

Let $N=2^k$. Ordinary Andreev has independent table bits $x_c$ indexed by $c\in\{0,1\}^k$, and $k$ address blocks $a_i$ of $m$ bits. Put $s_i=\sum_j a_{i,j}$, $b_i=s_i\bmod2$, and $A_{k,m}(x,a)=x_b$. Total input length is $n=N+km$. In the exactly balanced family $km=N$, $n=2N$; exact balance with integer $m$ requires $k\mid2^k$ (so positive $k$ is a power of two). Floor/padding variants require explicit treatment.

A bottom threshold gate is $[w\cdot(x,a)\ge t]$. The top threshold gate reads bottom outputs **and raw input bits**, with arbitrary real coefficients unless restricted explicitly. Many experiment reports count $S$ bottom gates; total size is $S+1$. Lean circuit size includes all gates. Wires generally count nonzero aggregated coefficients, not coefficient magnitude; majority literal multiplicities are a separate resource.

Average-case agreement is $1/2+\varepsilon$ under the uniform distribution on **all input bits**. A sigmoid output-separation parameter is a margin, not this agreement advantage. Ordinary Andreev and code-based/generalized Andreev are different functions.

## 2. Exact upper bounds

### Foundational quadratic construction

For table signs $\xi_c=1-2x_c$ and characters $\chi_S(c)=(-1)^{\sum_{i\in S}c_i}$ define

$$X_S=\sum_c\chi_S(c)\xi_c,\qquad t_S=\sum_{i\in S}s_i.$$

Character cancellation gives $\sum_S X_S(-1)^{t_S}=N\xi_b$. Since $X_S$ is even for $k\ge1$, with $\varphi(u)=(-1)^u u$,

$$\varphi(X_S+t_S)+\varphi(X_S-t_S)=2X_S(-1)^{t_S}.$$

Each function on a finite integer interval telescopes into threshold indicators. This yields $4N^2+kmN$ bottoms plus one top: $(5/4)n^2+1$ at balance. Bottom weights are $0,\pm1,\pm2$. No intermediate forms/parities are computed in extra layers: substitute affine forms directly into each gate. The zero-address-bit case is a trivial input bit. See `workspace/andreev_quadratic_upper_bound.tex`; this older PDF is not the latest bound.

### Better algebraic constructions

The free-affine-top-term and asymmetric product identities reduce the count further. A $(3/4)n^2$ construction is formalized and merged (PR #2813). The strongest general **research construction** currently recorded is $d''$:

$$S_{d''}=\frac{N^2}{2}+\frac34kmN-
\begin{cases}kN/2&m\text{ even},\\kN/4&m\text{ odd}\end{cases}
+O(N+km).$$

At balance its leading count is $5n^2/16$, with lower-order savings. This is still quadratic. Detailed proof, exact formula, generator code and checks: `experiments/push_upper/report.md`, `constr3.py`, and `experiments/linear_trick/`. The paper PDF can lag these reports. Do not describe every later research construction as already Lean-formalized.

### Existing average-case upper bounds — predating Astra

The earlier paper already proves agreement $1-\delta$ with $O(N\sqrt{n\log(N/\delta)})$ gates, hence $O(n^{3/2}\sqrt{\log(n/\delta)})$ at balance. It also proves the size–advantage tradeoff $O(\varepsilon^2n^{3/2}\sqrt{\log n})$ gates and $O(\varepsilon^2n^{5/2}\sqrt{\log n})$ support wires for advantage $\varepsilon$ in the documented range. See `workspace/threshold_paper/paper.tex`, theorem labelled `thm:avgupper`, and `workspace/andreev_depth_two_bounds.md`, Theorem 2. The approximation method already truncates staircases using concentration and restricts to a subset of characters to tune advantage. Near-matching average-case exponents and epsilon dependence therefore predate the Astra investigation. The later Astra mixed-sign truncation is a variant/rediscovery of this bound, not a new asymptotic upper bound.

### New coarse-Fourier family, fixed $k=3$

`experiments/mixed_upper_sol/report.md` and `constructions.py` give, for every $m\ge1$,

$$S_3(m)=6\lfloor m/2\rfloor+6m+\lfloor3m/2\rfloor+26$$

bottoms plus one top. This has slope $21/2$ and improves an inherited fixed-$k=3$ slope $27/2$. It does **not** improve the growing-$k$, balanced quadratic constant.

The new idea is sign-only reconstruction from coarse Walsh amplitudes. Put $h_S(x)=\sum_c\chi_S(c)x_c$ and $H_{S,r}=[h_S\ge r]$. Use thresholds $r=0,1$ for the six singleton/pair characters and $r=0$ for the triple: 13 amplitudes. Set $a_S=18$ for pairs and $15$ otherwise, and $D(x)=6(x_0+x_7)+8\sum_{c\ne0,7}x_c-30$. Then

$$F(x,b)=D(x)+\sum_{(S,r)}a_S\chi_S(b)(2H_{S,r}(x)-1)$$

satisfies $(2x_b-1)F\ge15$ on all 2048 table/address pairs, checked with integers. Gates $[6t_S+h_S\ge12j+r]$, together with table-only $H$, realize each product for every $m$. The report proves the identity and gives explicit weights/counts. These gates are **block-symmetric/sign-coherent**. The user now permits pursuing this direction only via genuinely mixed in-block signs toward subquadratic size.

### Generator-SMT campaign: six-gate uniform improvement at k=3

`experiments/generator_smt_sol/report.md` and `uniform_integer_certificate.json` improve the preceding fixed-k construction to

$$S_3^{\mathrm{new}}(m)=6\lfloor m/2\rfloor+6m+\lfloor3m/2\rfloor+20$$

bottoms plus one top for every $m\ge1$. A rational score on the inherited thirteen Walsh amplitude channels has seven nonzero table-only corrections instead of thirteen. Exact integer checking of all 2048 table/parity pairs and an all-m ladder identity prove ordinary-Andreev correctness. Explicit m=3,4,6 witnesses have 48,62,83 bottoms; m=3 also passes the independent arbitrary-table symbolic miter, while m=4 and m=6 symbolic timeouts remain UNKNOWN. The proof was independently reviewed in `bounce/review.md`. This is a six-bottom additive improvement at fixed k=3, with unchanged slope21/2 and no balanced asymptotic improvement. No Lean formalization is claimed.

The engine genuinely quantifies every acyclic size-r binary-LUT generator description, feeding only its evaluated table and raw addresses to one fixed threshold circuit. r1/r2 family successes are not ordinary-Andreev claims. A canonical AND/XOR representation with complemented edges preserves the family for r>=1 but did not show a checker speedup. See the full report for exact quantifiers, tested matrix, family-only witnesses, counterexamples and the restricted separable-ladder architecture barrier.

### Small exact/constructive instances

- General full model: $A_{2,1}$ and $A_{2,2}$ have exact minimum three bottoms, with direct top inputs allowed.
- A recovered ten-bottom $A_{2,4}$ construction restricts to ten bottoms for $A_{2,3}$. These are upper bounds, not claims of optimum. Witnesses/formulas: `experiments/mixed_upper_sol/explicit_2_3.json`, `explicit_2_4.json`, report §3.
- At $k=1$, an explicit $\lceil m/2\rceil$-bottom sign-correct circuit is known; small unrestricted optima match for tested $m$.
- A seven-bottom candidate for $A_{2,3}$ has 56 errors out of 1024 inputs, all involving block pattern `011`. It is **not a construction**. Exact witness/diagnostics: `experiments/variants_sol/`. One-added-gate repair with all seven fixed was impossible; broader bounded runs were UNKNOWN.
- Nine-bottom $A_{2,3}$ pool search in the later run was UNKNOWN, not UNSAT.

## 3. Lower bounds and their status

### Unrestricted THR∘THR

The formalized fixed-weight restriction/counting method proves explicit inequalities that yield

$$\Omega(\varepsilon^2 n^{3/2}/\log^2n)\text{ gates},\qquad
\Omega(\varepsilon^2 n^{5/2}/\log^{5/2}n)\text{ support wires}$$

at balance and $\varepsilon\gtrsim\log n/\sqrt n$. Worst case is $\varepsilon=1/2$. The Lean code proves finite inequalities; asymptotic interpretations are documented. PR #2377 is merged. The core improvement counts threshold shifts of the **original fixed bottom weights**, rather than arbitrary LTFs, and averages square roots instead of using a lossy Markov step.

A later hand derivation retains original **top weights** too. For exact survivor count $q$ the restricted family has at most $\binom Sq(N+1)^{q+1}$ functions. This extends the **gate** bound to $\varepsilon\ge C\sqrt{\log n/n}$ in the derivation in `workspace/worst_case_notes.md`. Treat this as a hand proof pending its own formalization/check, not as covered automatically by PR #2377. For wires, absorbing single-variable gates changes live top coefficients, so that extension does not transfer directly.

The classical source is Kane–Williams, arXiv:1511.07860v1: gate/wire average-case lower bounds originally have $\varepsilon^3$ and log powers $3,7/2$. Source-proof corrections are preserved in `workspace/kane_williams_erratum.md`. Do not infer novelty of every improvement from an exhaustive literature search; novelty notes have their own limits.

### Sign-coherent and mixed-sign restrictions

A gate is sign-coherent if all its weights within each address block have one sign, possibly different signs across blocks/gates. Block-symmetric gates are a subclass. Cube/table entropy plus a single-crossing lemma gives $\Omega(n^2/\log^3 n)$ for coherent circuits at balance. Complete proof and independent review: `experiments/push_lower/report.md`, `experiments/review_lower/report.md`. The original report contains interpretation errors and regime caveats; the reviewer explicitly corrects them.

Important facts/corrections:

- The coherent cube-split bound is $m^k-(m-1)^k$, attained for every parameter pair. A single-crossing ingredient is classical; the report distinguishes its source from the application.
- The unconditional general closed form must use a minimum with $N^2$ or the self-consistent entropy inequality; the balanced bound is unaffected.
- Claims that *all* loss is in the per-cube entropy count, or that the method proves a universal barrier, were overstated. Its barrier has a specified proof template.
- Random mixed-sign $\pm1$ gates obstruct uniform per-gate survival improvements. A few globally fixed signed views do not supply the diversity needed for a fixed-power subquadratic improvement. Runs/sign-pattern extensions and limits are in `experiments/mixed_sign/report.md`.
- Simply changing $t_S$ to a signed sum preserves parity but does not shrink its full range. Independent ladders still cost $\Theta(m\sum_S|S|)=\Theta(N^2)$ at balance even with constant-many amplitudes per character.
- The simple equal-weight Walsh-sign clipping extrapolation fails at $k=4$ on 14336 of 65536 tables (`mixed_upper_sol/frontier.log`). This refutes that rule, not every coarse Fourier design.
- Restricting tables to $x_c=y\oplus |c|$ gives parity on $km+1$ bits with the same gate budget. This is useful at fixed $k$, but does not prove a general exact linear parity lower bound. Small solver optima do not establish the conjectured formula for all sizes.

### Majority and exact-sum research

Latest report: `experiments/maj_sol/report.md`. It distinguishes majority literal multiplicity, bounded integer coefficients, unit top weights, and unrestricted real thresholds. Do not identify these models without charging duplication and constants.

- New hand proof: in the **exact-top-sum** model, if every gate's nonzero address weights have a common magnitude within that gate (arbitrary mixed signs), then $S\ge\binom{k}{\lfloor k/2\rfloor}=\Omega(N/\sqrt k)$. The proof is a joint table/address Fourier matrix rank argument; there is a quantitative approximation extension. This is not a stronger balanced unrestricted-real bound.
- A proposed pointwise $O(V/m)$ smoothness lemma is false even for balanced $\pm1$ weights. The hoped-for $\Omega(Nm/V)$ gate theorem remains unresolved.
- The actual $d''$ coefficient/multiplicity cost is $\Theta(n^3)$ at balance. Cloning to eliminate repeated top gate-output wires changes gate and literal-wire costs substantially; see the exact totals.
- The new finite exact-sum minimum at $(k,m)=(1,3)$ with address magnitudes at most one is four bottoms. Do not extend that optimum to unrestricted magnitudes.
- Known-source Paturi–Saks plus the parity restriction gives a fixed-$k$ polynomial-weight consequence $\Omega(m/\log^2m)$. This is a transfer from prior work, not a new unrestricted balanced bound.
- Low communication limits these methods' potential but does **not** imply that they yield no polynomial lower bounds. The earlier chat overstated that point; the latest report corrects it.

## 4. Other functions and sigmoid comparison

Generalized/code-based Andreev $B_n$ is distinct from ordinary $A$. Depth-three/top-fan-in applications and $B_n$ development are discussed in `workspace/kw_applications.md`, paper sources, and the formalization PR references.

The linked preprint is Li–Reichman–Williams–Wu, *New Gate, Weight and Wire Complexity Bounds for Sigmoid Neural Networks*, STOC 2027 submission 673:
https://github.com/sigact-stoc/stoc2027/releases/download/papers-1/673.pdf

Its closest result concerns generalized Andreev and depth-three sigmoid circuits, with bounded upper-layer parameters and noticeable output separation. Its margin is not agreement advantage. Our small-integer polynomial-weight threshold upper constructions combine with its threshold-to-sigmoid simulation (Lemma 3.13) to give polynomial-weight, same-depth sigmoid upper bounds. Our THR lower bounds do not automatically transfer back through its polynomial-overhead reverse simulation. No direct subsumption or new optimal sigmoid bound was established.

## 5. Lean and paper provenance

Authoritative exact public snapshots: `formalization/pull_requests.json`.

- https://github.com/cslib-community/complexitylib/pull/2377 — merged; logarithm-saving Andreev lower-bound pipeline and updated abstract.
- https://github.com/cslib-community/complexitylib/pull/2813 — merged; $3n^2/4$ exact circuit.
- https://github.com/cslib-community/complexitylib/pull/2814 — merged; approximate-majority/top-fan-in applications.
- https://github.com/cslib-community/complexitylib/pull/2816 — open at snapshot; $B_n$ depth-three/log-saving work. Patch saved as `formalization/pr-2816.patch` with base/head OIDs in metadata.

The revised paper now records the merged PRs and clearly separates Lean coverage of earlier upper bounds from the two new upper-bound proofs. The $5n^2/16$ construction and improved mean-square approximation proof are included in the paper but not formalized in Lean. Other research refinements remain in their reports; do not infer Lean coverage from their appearance in this archive.

## 6. Completed mixed-sign coarse-Fourier search

`experiments/coarse_mixed_general/report.md` gives an exact localized coarse-product identity with mixed signs inside every active block. A window costs its retained integer layers plus two endpoints and has no uncancelled linear tail. A varying-width mask identity cancels arrangement dependence exactly; saved rational witnesses and checks establish this finite subproblem. These witnesses are more expensive than the existing full ladders.

The report also proves an exponential mask-support obstruction for exact reconstruction by translates of a single middle-layer kernel. This is restricted to that architecture, not an impossibility theorem for mixed threshold circuits or variable-width pooling. No subquadratic ordinary-Andreev construction was found. Efficient pooling across growing-k characters remains unresolved. All associated jobs finished before archival.

## 7. Astra lower-bound proposals — pending independent review

The completed report `experiments/lower_astra/report.md` supplies three new hand proofs, exact finite guardrail checks, counterexamples and primary-source references. These are provisional research claims, not independently reviewed or Lean formalized.

- A fixed-design VC/Rademacher estimate for the fixed-direction, fixed-top restricted class, with an adaptive survivor-count argument, extends the existing unrestricted gate bound $\Omega(\varepsilon^2n^{3/2}/\log^2n)$ to $\varepsilon\ge C/\sqrt n$. The central inequality is $2\varepsilon\le C\sqrt{(B\log(S+1)+2)/N}$, with $B$ the mean number of survivors. It changes the advantage range, not the constant-advantage exponent or logarithmic denominator. No wire-range extension is claimed. A zero-bottom table-majority circuit already has advantage $\Theta(N^{-1/2})$, so the endpoint needs a sufficiently large constant and an additive subtraction in the exact inequality.
- Parity-fiber averaging plus an all-orthants subspace lemma gives $S\ge\binom{k}{r}$ for every $1\le r\le k$ at actual THR-at-top when $m\ge2$ and each bottom gate has one common absolute value among its nonzero address coefficients. It also forces full rank of each level's block-sign/support signature matrix. This removes the exact-sum requirement from the earlier restricted result; it is not a stronger balanced unrestricted size bound. Multiple magnitudes break rank one, and binary-place weights make even one gate's threshold-shift span full, so an unrestricted extension must exploit affine dependence of shifts on the table.
- A per-block min-to-max crossing decomposition and concentration by the live coordinate's own weight rank gives arbitrary-weight count-restriction survival $O(k/\sqrt m)$. Combined with the existing entropy/runs argument, this saves $\sqrt{\log n}$ in a mixed-gate requirement, yielding $\Omega(n^{3/2}/\log^{5/2}n)$ sufficiently mixed gates under the report's size assumptions. This count restriction does not generate uniform raw addresses, so it is separate from the first result's uniform average-case restriction.

The unrestricted worst-case exponent, support-wire bound, and coherent quadratic conjecture remain unchanged. The upper-bound Astra investigation is still pending at this update.

## 8. Astra upper-bound findings — exact and distributional results

The completed report `experiments/upper_astra/report.md` contains a hand-proof distributional construction, exact finite certificates and explicit open construction targets. These are not Lean formalized and the analytical claims await independent review. No exact subquadratic ordinary-Andreev bound was obtained.

For uniform independent raw table/address inputs, agreement at least $1-\delta$ is obtained with $O(N\sqrt{(N+km)\log(N/\delta)})$ bottoms plus a top. At balance this is $O(n^{3/2}\sqrt{\log(n/\delta)})$. The construction centers differently mixed-sign address sums and truncates the original Walsh-product ridge staircases. Hoeffding concentration and a union bound show that every retained argument is in range with probability at least $1-\delta$, where the score equals the exact target score. Every indicator is an actual raw-input LTF; no intermediate features are supplied. For fixed error $0<\delta<1/2$, these are the same $3/2$ exponent and logarithmic gap already obtained in the earlier paper. This Astra variant does not improve the existing asymptotic average-case upper bounds; the prior construction also provides an epsilon-squared tradeoff not developed in this report. No literature-priority claim is made. This does not match the dependence on arbitrarily small advantage, nor prove exact correctness. Eliminating every exceptional input by concentration alone restores quadratic size. Economical shared tail repair remains the missing lemma.

For $k=4$, writing $X_S=\sum_c\chi_S(c)(2x_c-1)$ and $q_r(t)=[t\ge r]-[t\le-r]$, the new exact certificate is

$$F=4X_\varnothing+\sum_{S\ne\varnothing}\chi_S(b)(11q_2(X_S)+32q_4(X_S)).$$

Its minimum signed score is 43 on all independent tables and addresses. The parent independently rechecked all 65536 tables at address zero with a separate Walsh-transform implementation; translation symmetry and oddness extend to every address. A direct mixed-ladder realization costs $64m-16[m\text{ odd}]+120$ bottoms, so it does not improve the strongest inherited circuit bound. The report also proves that fixed unequal character weights cannot rescue the specified odd sign-only Walsh rule, even with an arbitrary table intercept; this is a narrow architecture obstruction.

Two exact targets are developed: joint margin-sensitive mixed windows, and an address-halfspace dictionary with kernels $K_c(a)$ satisfying $K_{b(a)}(a)>\sum_{c\ne b(a)}|K_c(a)|$. The latter condition is necessary and sufficient for a score linear in independent table signs. Gating each dictionary feature by one table bit gives a circuit cost $H+\operatorname{nnz}(\beta)$; no economical dictionary meeting the condition is yet known.

Both requested Astra tasks have completed. Their reports leave the exact balanced upper bound, unrestricted worst-case lower exponent, and wire bound unchanged.

### Correction to the Astra upper-result announcement

The parent initially presented Astra's truncated mixed-ridge bound as a new matching-exponent average-case advance. That was incorrect: the pre-existing paper and overview already state the same bound and the stronger epsilon-squared tradeoff. The curated summary had omitted that prior upper result from the Astra handoff. Preserve the agent report as provenance, but do not claim an improved average-case upper bound from it. Its additional contributions are an explicit mixed-sign variant, the exact finite k4 certificate, the specified sign-only obstruction and proposed exact-construction targets. None improves the known asymptotic upper bounds. The lower Astra advantage-range extension remains a separate provisional improvement pending review.

## 9. Astra upper round 2: genuine average-case logarithmic improvement

`experiments/upper_astra_round2/report.md` gives a new hand-proof improvement over the pre-existing average-case theorem. It has explicit raw-input LTF formulas and deterministic nonuniform existence via fixed-mask averaging. It is not Lean formalized and has not received a separate full independent referee review. The parent inspected the central cancellation/conditioning argument and separately verified vanishing cross-character moments on every k=m=2 table/address and mask marginal at radius 2.

For uniform independent table/address bits and balanced $km\asymp N$, agreement $1-\delta$ now has an upper bound

$$S=O(n^{3/2}\sqrt{\log(1/\delta)}),\qquad 0<\delta\le1/2,$$

plus one top gate. This replaces the OLD $\log(n/\delta)$ inside the square root. Constant error consequently uses $O(n^{3/2})$ bottoms, a genuine $\sqrt{\log n}$ saving. Polynomially small error retains the old asymptotic order. The earlier Astra round's approximation was a rediscovery; this second round has a different, stronger proof.

For $N^{-1/2}\le\varepsilon\le1/8$, selecting a subset of characters and subcube majority gives

$$S=O(\varepsilon^2n^{3/2}\sqrt{\log(1/\varepsilon)}),\qquad W=O(\varepsilon^2n^{5/2}\sqrt{\log(1/\varepsilon)}).$$

For $1/8<\varepsilon<1/2$, use the error bound with $\delta=1/2-\varepsilon$. This improves the old square-root logarithm for constant or subpolynomially small advantage; polynomially small advantage retains the same asymptotic order. No advantage-dependent logarithm saving is claimed uniformly as epsilon approaches one half.

The change is ZERO-truncation of Walsh-product staircases and independently chosen address masks per character. Conditional on a table and address, masks make distinct character errors independent; their conditional means have the form $\chi_S(b)g_S(X_S)$. Averaging the uniform raw address kills cross terms by character orthogonality, without assuming Walsh coefficients are independent. The total mean-square error is therefore the sum of diagonal errors. Subgaussian tail second moments and Markov yield a radius $O(\sqrt{N\log(1/\delta)})$ instead of $O(\sqrt{N\log(N/\delta)})$. Averaging selects one fixed circuit; no run-time random inputs or mask-dependent circuit per input are allowed. Genuinely mixed/diverse masks can be imposed in the balanced growing-k regime by conditioning mask selection, at constant-factor cost.

The finite theorem uses $t=2^r$, $V=N+rm/4$, radius $R=\lceil4\sqrt{V\log(16V/(t\delta))}\rceil$, at most $4(t-1)(R+1)$ bottoms, and agreement $1/2+p(N/t)/2-\delta$. For truncated subcube-majority output, the top threshold is shifted to avoid zero-margin ties. See the report for exact p, all gate coefficients, and mixed-mask conditioning.

No exact upper bound improves: general leading $5n^2/16$, fixed-k3 +20 formula and small k2 witnesses remain current. Sparse selector LP witnesses were valid but noncompetitive. The report states the remaining exact shared-tail repair lemma. Every task-owned process finished, and code, witnesses, audits and logs are archived.


## 10. Logged comparison: new average-case bounds versus the paper

**Status:** new Astra upper/lower analytical results are hand proofs pending full independent review and Lean formalization. This entry records the comparison requested by the user. All bounds concern balanced ordinary Andreev under uniform independent raw table and address bits, with arbitrary real depth-two threshold circuits and direct raw-input wires at the top. Gate upper counts are bottoms plus one top. Let $N=2^k$ and $n=N+km$ with $km\asymp N$.

| Requirement | Earlier paper / archived theorem | New upper bound |
|---|---|---|
| Agreement $1-\delta$: gates | $O(n^{3/2}\sqrt{\log(n/\delta)})$ | $O(n^{3/2}\sqrt{\log(1/\delta)})$ |
| Agreement $1/2+\varepsilon$: gates | $O(\varepsilon^2n^{3/2}\sqrt{\log n})$ | $O(\varepsilon^2n^{3/2}\sqrt{\log(1/\varepsilon)})$ |
| Agreement $1/2+\varepsilon$: support wires | $O(\varepsilon^2n^{5/2}\sqrt{\log n})$ | $O(\varepsilon^2n^{5/2}\sqrt{\log(1/\varepsilon)})$ |

The error comparison uses $0<\delta\le1/2$. The displayed advantage comparisons use $N^{-1/2}\le\varepsilon\le1/8$. For $1/8<\varepsilon<1/2$, use the error bound with $\delta=1/2-\varepsilon$; do not extrapolate the small-advantage formula to near-perfect agreement.

For constant error or constant advantage, the upper bounds save $\sqrt{\log n}$. For polynomially small error or advantage, the asymptotic order stays the same. Neither result improves the exact-computation upper bound. The improvement comes from independent fixed-mask cancellation of cross-character truncation-error moments and an L2 estimate, replacing the old union bound. Masks are chosen once per circuit, not per input.

The existing gate lower-bound expression is unchanged:

$$S=\Omega(\varepsilon^2n^{3/2}/\log^2n).$$

At constant advantage, the gate upper/lower logarithmic gap shrinks from $\log^{5/2}n$ to $\log^2n$. The support-wire lower-bound expression remains $\Omega(\varepsilon^2n^{5/2}/\log^{5/2}n)$, so its constant-advantage logarithmic gap shrinks from $\log^3n$ to $\log^{5/2}n$. These compare asymptotic expressions, not numerical sizes or hidden constants.

Separately, the new lower hand argument extends the gate advantage range to $\varepsilon\ge C/\sqrt n$, compared with the paper's conservative formalized range $\varepsilon\ge C\log n/\sqrt n$ and the intervening hand-derived $C\sqrt{\log n/n}$ range. No corresponding wire-range extension is claimed. A zero-bottom table-majority circuit already achieves advantage $\Theta(n^{-1/2})$, so the sufficiently-large-constant qualifier is essential.

For the original Kane–Williams paper, the stated lower bounds are $\Omega(\varepsilon^3n^{3/2}/\log^3n)$ gates and $\Omega(\varepsilon^3n^{5/2}/\log^{7/2}n)$ wires. Its stated range is $\varepsilon\gg\sqrt{\log n/n}$; the archived erratum discusses proof-range caveats. Our earlier lower-bound work had already improved the epsilon dependence and logarithmic denominators. The present upper round supplies an additional upper-bound improvement, not a new change to those lower-bound expressions. Source: [Kane–Williams, arXiv:1511.07860](https://arxiv.org/abs/1511.07860).

Local sources: `workspace/threshold_paper/paper.tex`, theorem `thm:avgupper`; `workspace/andreev_depth_two_bounds.md`, Theorem 2; `experiments/upper_astra_round2/report.md`; `experiments/lower_astra/report.md`. Sections 7 and 9 above retain proof status, the finite theorem, and restrictions. Section 8 and its correction retain the fact that the FIRST Astra approximation report merely rediscovered the prior upper bound.


## 11. Creative exact Astra round: verified finite improvements

The user requested only exact worst-case upper bounds, encouraging entirely new architectures, large weights and varied mixed signs. The completed report and raw-coordinate witnesses are in `experiments/exact_creative_astra`. The parent reran `verify_final.py` on all four saved witnesses, without solver calls; every check passed. These are exact upper bounds, not optimum claims or Lean-formalized results. No literature-novelty claim is made.

| Instance | Previously supplied construction | New bottoms | Total including top |
|---|---:|---:|---:|
| $A_{3,2}$ | 41 | 8 | 9 |
| $A_{3,3}$ | 48 | 32 | 33 |
| $A_{3,4}$ | 62 | 36 | 37 |
| $A_{4,4}$, exactly balanced | 370 from `count_dpp(4,4)` | 256 | 257 |

The first three checks directly evaluated every table/address input: 16384, 131072, and 1048576 inputs respectively. The last checks every one of 65536 raw addresses and computes exact score extrema over all independent table bits, certifying all $2^{32}$ inputs. All arithmetic is integer; thresholds use >=. The reported integer classification gap handles zero positive-class scores correctly and is not always a strict signed margin for the unshifted top score.

**Permutation-rank cancellation:** when $m=2$, encode the two address columns as integers $U,V$. For each label $c$, one gate compares $U$ against $V\mathbin{\mathrm{xor}}c$, using table bit $x_c$ to decide equality. These comparison targets permute $0,\ldots,N-1$, so their strict comparison count is exactly U. Hence $\sum_cg_c=U+x_b$, and a raw affine top correction extracts the selected bit. This proves $S\le N$ for every k at m2. The general paired-column extension gives $N^{\lceil m/2\rceil}$ bottoms; it is not competitive at balance. Address weights for m2 are at most $2^{k-1}=N/2$: exponential in k, but polynomial in total input length. The construction uses genuinely different within-block sign patterns.

**Monochromatic hyperplanes:** positional weights flatten simultaneous Hamming-distance equalities, yielding raw-address hyperplanes containing addresses of just one parity label c. Paired gates can contribute $(2x_c-1)[L(a)=0]$ exactly. More efficiently, one-sided gates with positive top weights plus a raw affine correction need only satisfy two worst-case sign inequalities, rather than exact tail cancellation. A bounded support search yields the 32- and 36-bottom certificates above. The A4,4 certificate uses an explicit eight-word mask cover and two gates per plane, giving 256 bottoms. Its weights are small, with address magnitudes at most 27. Both one-sided certificates also have small integer weights.

The report proves an exact nonuniform general cover bound. For $r=\lfloor m/2\rfloor$ and $p_m=\binom mr/2^{m-1}$,

$$S\le2N\left\lceil\frac{k(m-1)\log2+1}{p_m^k}\right\rceil.$$

For fixed small m this gives subquadratic unbalanced families (m2 has the stronger rank construction). At balanced growing m the cover estimate is superpolynomial in N, so it does not improve the general exact bound. Do not extrapolate the finite balanced A4,4 saving into a balanced subquadratic family. The general leading $5n^2/16$ benchmark, fixed-k3 all-m slope21/2, A3,6=83 and known k2 witnesses remain unchanged unless separately improved.

The next proposed finite experiment is one-sided positive-margin selection on the 128-plane A4,4 dictionary, starting with its guaranteed 256-bottom paired cover. The asymptotic missing piece remains sharing comparisons across labels, potentially with gates depending on several independent table bits, while proving a simultaneous worst-case sign margin. No task-owned solver remains running. All artifacts are preserved.


## 12. Asymptotics-only creative restart: no improvement

The completed report `experiments/asymptotic_creative_astra/report.md` explicitly obtains **no balanced asymptotic exact upper-bound improvement**. The current general exact leading bound remains $5n^2/16$. No new finite-size or approximate result was used to claim progress on this request. The parent reran the saved standard-library exact checks successfully; analytical statements remain hand proofs, without independent referee review or Lean formalization.

An exact rank-retrieval identity can query a threshold-encoded table row $h_{T(a)\bmod N}(x)$ with $D+1$ bottoms when an integer affine raw-address form satisfies $0\le T\le D$. Taking $T=\sum_i2^is_i$ has range $O(mN)$, which would be attractive at balance, but its binary residue is not the block parity vector because of carries. The proposed repair used a few signed/permuted positional views and arbitrary nonlinear table codes.

The report supplies a scalable counterexample defeating that specific repair whenever $k\ge2$ and $m-1>2^L$, where L is the number of views. Two coordinates per block share their L-view sign signature. Pair activation preserves block parity while making each query residue uniform on a parity coset. Averaging any proposed score over those activations leaves only an affine function of the block parities; it cannot represent a legitimate XOR table. Thus $L=o(k)$ cannot give the intended logarithmic saving in that architecture, even with arbitrary table encodings and large weights. This is an obstruction to one proposed upper-bound mechanism, not a lower bound for general circuits.

The remaining proposed architecture uses separate raw-address hyperplanes $Z_r(a)=0$ to activate threshold code rows $\operatorname{sgn}(\ell_r(x))$, with different address weights for each row. An exact two-bottom identity implements each product. Its unproved requirement is

$$ (2x_b-1)\sum_{r:Z_r(a)=0}v_r\operatorname{sgn}(\ell_r(x))>0 $$

for every independent table and address, using $R=O(mN)$ rows. If such a family existed, its $2R+1$ gates would give $O(n^2/\log n)$ at balance. No such family was constructed, and no evidence that the requisite incidence/decoding lemma holds is claimed. The compiler alone is not an asymptotic construction. The missing ingredient is an exact all-table decoding identity for the row sets activated at every address, with a provably economical shared row family.

Artifacts preserve the rank compiler, exact two-gate identity, illustrative three-bit threshold code and scalable counterexample checks. No solver or background job was launched by this task. User scope remains exact balanced asymptotics; further finite-record or approximation searches are outside that scope unless newly requested.


## 13. Second asymptotic creative pass: scalar Walsh-compression blockers

`experiments/asymptotic_creative_astra_pass2/report.md` records **no balanced exact asymptotic improvement**. The developed route was separable nonlinear Walsh decoding $F_\phi(y,b)=\sum_S\chi_S(b)\phi(h_S(y))$. Its failure is shown by explicit scalable tables, not merely solver timeouts. These hand proofs are architecture-specific and not unrestricted threshold lower bounds. The parent reran the saved exact spectrum, gate-identity and modulation/spike checks successfully.

A five-point pattern in four binary coordinates has Walsh spectrum ten copies of -2 and six copies of 6. Repetition shows that hard clipping at any $B=o(N)$ fails universal sign decoding. Puncturing produces a defect $D_\phi=\phi(10)+10\phi(2)-5\phi(6)$; when positive and $\phi(t)=o(t)$, its linear-in-N negative contribution defeats the decoder. This rules out fixed sublinear powers and fixed logarithmic shrinkers, with the report's additional repetitions for the latter. An affine-repair lemma rules out rescuing these specific decoders with arbitrary affine raw-table/address terms at the top. It does not rule out multiple coupled coefficients, different bases, channel-dependent rules, asymmetric encodings or general mixed-sign circuits.

The report also audits raw-gate costs: scalar amplitude compression alone does not remove the address-interaction cost, and nonlinear compressed forms cannot simply be substituted into identities requiring affine table forms. Thus even a successful table-only decoder would need separate subquadratic gate accounting.

A proposed alternative uses nonlinear label permutations whose decoder characters expand into at most four ordinary Walsh characters. Same-control shears share a fixed slice on which the same puncture remains an obstruction. Different controls/global mixing have not been resolved, and sparse character expansion alone does not shorten the full address ladders. No positive asymptotic construction is claimed.

The new blocker context was delivered to the currently running coefficient-language Astra task for its original language-design assignment. It is information for design, not a separate requested review. All task-owned processes from this completed pass finished. Report, checks and exploratory probes are archived.


## 14. Coefficient-rule language design and prototype

The completed Astra design is archived in `experiments/coefficient_language_astra/report.md`, with a standard-library compiler prototype `rules.py`. It is a proposed synthesis infrastructure, not a new asymptotic circuit upper bound. The parent reran all eight regression tests and the three fixed-candidate Z3 miter checks: all expected results passed (two correct m2 rank fixtures UNSAT, intentionally false m3 extension SAT). No grammar-search/CEGIS learner has yet been implemented in this prototype.

The recommendation is a portfolio of two main languages sharing an exact raw-circuit format, checker, cost auditor and raw counterexample corpus:

1. **Index programs with affine numerical holes.** Every bottom/top/direct coefficient has the form $f_0(z)+\sum_q\theta_q\phi_q(z)$, where z contains public gate/input/size indices, and public feature programs support bit relations, irregular branches, positional scales, mixed masks and coupled multi-table-bit rows. One finite program and numerical tuple are shared across sizes. Fixed structural choices leave a concrete-example learner in Boolean QF_LRA; learned top coefficients times gate indicators are represented with ITE, not nonlinear real products. Unknown count can be independent of n/S, but sampled activation Booleans still scale as sum over sizes of E_s S_s.
2. **Additive atoms with raw-LTF contracts.** Atoms include unrestricted raw ridge gates, row-dependent threshold-code slices, mixed localized windows and rank/finite-difference identities. Their outputs may be added/scaled at the top but not fed into new bottom gates or multiplied. Exact raw expansions and unmerged costs prevent hidden layers or free preprocessing. Independent per-character reconstruction is not required. This language currently lacks the all-size shared-incidence/cancellation theorem needed for subquadratic cost.

Tune a vector of nested resource bounds: types, index-program DAG size, numerical holes, decision depth, index-bit capabilities, index interaction arity, optional factor width, support-description complexity, magnitude profiles, rational/integer parameter budget, emitted coefficient-bit budget and gate-domain menu. Use “at most” bounds and padding to justify nesting; replacing a menu is not automatically an enlargement. Finite-state index transducers, decision programs and generated tensor factors are complementary portfolio choices rather than a single ordered scale. Tensor factors learned jointly require nonlinear arithmetic; finite factor menus or fixing factors keep simpler learners but are deliberately incomplete proposal methods.

Concrete numerical accounting: a free S-bottom circuit has S(n+2)+n+1 real unknowns. With T types and q holes per coefficient field, Language A has (4T+3)q numerical holes. At n32,S128 the free model has4385 unknowns; T2,q2 uses22 holes. This does not predict wall time: every sample still contributes128 activation choices, and a large grammar may be worse than the free model on tiny instances. A shared parameter model is a genuine restriction, not WLOG completeness.

Important soundness requirements: retain exact threshold ties/strict negative inequalities; independent unit-margin rescaling can break shared rules and is NOT generically WLOG. Fixed public powers/mod/products are evaluated outside SMT, while unknown bases, factors, divisors or multipliers must be costed in their actual harder theory. Avoid bit-vector overflow and exponentially long output integers. Every checker retains arbitrary independent raw table/address inputs. UNSAT must name the searched grammar/parameters/sizes; it is not an unrestricted lower bound. Finite multi-size correctness does not prove all-size uniform correctness.

The proposed next implementation is fixed-skeleton affine-hole CEGIS with small feature menus, multiple magnitudes/positional profiles and multi-table-bit rows available early, plus a separate atom compiler. Start training across n8/n17, extend to n28/n32, use holdout combinations and larger balanced sizes, and prove any eventual all-size invariant separately. All existing blockers, including both asymptotic creative-pass counterexamples, are accounted for with scope limitations; no scalar-shrinker or few-periodic-channel rediscovery should be counted as progress.

The compiler currently covers exact index/parameter evaluation, raw circuit generation/evaluation, m2 rank fixtures, slice/window atoms, common-reorientation diagnostics, SMT-LIB miter export, and resource guards. It lacks a production static type/scope checker, structural search, CEGIS learner, automata implementation, full rank-filter implementation and all-size proof engine. All artifacts are saved, and no task-owned solver remains running.


## 15. Shared-rule SMT experiment actually implemented and run

The user's request to run the experiment is completed. `experiments/uniform_rule_smt/report.md`, `experiment.py`, sample corpora, exact parameter models, event logs and `campaign_results.json` preserve an operational affine-rule multi-size CEGIS learner. No new exact ordinary-Andreev circuit or asymptotic improvement was certified. This is a fixed-feature grammar experiment, not a full AST-language search or a free unrestricted n32 optimization run.

Every universal checker uses independent raw table/address bits. Shared real numerical holes generate bottom table/address coefficients, thresholds, top coefficients and direct input terms. Exact >= ties and strictly negative false examples are preserved; no per-gate unit-margin normalization, bounded magnitude or generator-table restriction is imposed. Core targets are (k,m)=(2,2),(3,3),(4,3),(4,4), hence n8,17,28,32, with identical parameter tuples across sizes. Gate domains are T*N*m, so a valid constant-T all-size rule would yield n^2/log n; no such rule was established.

- A 14-hole positional/mixed-sign skeleton with 8/24/48/64 bottoms, and a 33-hole richer coupled-row skeleton with 16/48/96/128 bottoms, each timed out on its first 60-second call using187 initial examples across the four sizes. Activation Boolean counts were6872 and13744.
- A weak curriculum produced a partial fit in12.887s, but all hidden top coefficients were zero. Exact arbitrary-table miters refuted it at all sizes. Relearning timed out at60s.
- A strengthened curriculum seeded XOR-table raw-address corners, preventing a raw-affine-only solution. It fitted48 samples in39.463s, with all relevant hidden terms active, dense table rows and genuinely non-reorientable mixed signs. All four universal checkers again found counterexamples, adding16 points; relearning on64 samples timed out at60s. The saved model is REFUTED, not a circuit result.
- A balanced n32-only 64-bottom/14-hole run received a full300-second learner-call budget and returned UNKNOWN before producing a candidate. It had48 samples and3072 activation Booleans. This updates earlier statements that no sustained n32 shared-rule search had been run; it still is not unrestricted gate synthesis or an hours-long run.
- Two fixed-bottom top/direct-rule refits were UNSAT in0.0046s and0.0058s. These exclude only those particular frozen bottom rules and the declared shared top feature menu, not every top threshold over a library or the overall language.
- Calibration fitted three top-rule holes for the known m2 rank bottoms on all n4/n8 inputs and verified a held-out k3,m2 case. This is recovery of an inherited identity, not a new upper bound or optimum.

The final test suite passed four tests, including24 exact fixed-parameter learner/compiler comparisons, freezing preservation, known-rank/tie semantics and counterexample detection. Every SAT learner model was exactly checked on retained samples, and every returned counterexample was independently evaluated before insertion. Full actual sample sets are saved, including the two distinct initialization policies; replay commands name --legacy-samples for the older runs. No solver-owned process remains running, and no unrelated historical process was changed.

The result demonstrates that the shared-rule infrastructure works, but reducing numerical parameters alone leaves substantial activation-pattern branching. Only these specified skeletons/budgets were tested. UNKNOWN is not UNSAT, finite calibration is not all-size proof, and cheap fixed-bottom refitting does not solve the task of discovering useful bottom directions. The grammar design report's larger structural-search and all-size proof objectives remain open.


## 16. n64 small-gate UNSAT campaign

The user explicitly requested n64 feasibility checks with small gate budgets, aiming at UNSAT. These are unrestricted real-weight checks, not the previous coefficient-rule grammar. `experiments/n64_unsat/report.md`, exported SMT instances, corpora, restriction embeddings and campaign_results.json preserve the completed campaign. No asymptotic lower-bound improvement or optimum claim is made.

Two declared64-input targets were tested: equal-block standard A_(4,12), with16 table plus48 address bits, and an exactly balanced unequal-block variant with32 table bits and parity-block lengths (7,7,6,6,6). There is no exactly balanced equal-block instance at64. Do not conflate those definitions.

**Proved:** both targets require at least FOUR bottom gates, hence FIVE total gates. Fix the table to its character-parity values and all but eight raw address bits to zero. The resulting function is parity8. Exact unrestricted parity8/S3 SMT was UNSAT in5.283 solver seconds; the explicit256-point embeddings into both64-input domains were checked. The exported SMT2 replay was also UNSAT in7.367s. The restriction proof keeps bottom count, unrestricted real weights and direct raw top inputs unchanged. This is a rerun/transfer of the already-known small parity obstruction, not a new asymptotic theorem.

Direct balanced64 sample checks exclude S0, S1, S2 in2.667s,29.963s,59.641s respectively. They use arbitrary real parameters and no input-sign normalization. Every sample is a valid original input; exact UNSAT on that subset excludes a full circuit.

**Unresolved:** S4 direct checks on BOTH targets returned UNKNOWN after600s each. Valid full-target input-symmetry variants returned UNKNOWN after300s each. The balanced S5 check returned UNKNOWN after300s. A complete parity10/S4 restriction with2560 valid off-transition edge clauses also returned UNKNOWN after180s. None proves the next lower bound or supplies an upper witness.

Direct S4/S5 formulas use1152 actual inputs, unrestricted gate coefficients and real top/direct coefficients, and329/395 real parameters respectively. SAT would be exactly reevaluated and checked by an arbitrary-table/raw-address miter; none of the hard learner calls produced a SAT candidate. Only gate-output complement/permutation normalization is used by default. Optional nonnegative/block-sorted direct-address coefficients are WLOG for the full target through single-address flips with induced table-label permutation and within-block permutations. This does not assume common signs in bottom blocks. The report distinguishes full-target normal-form logic from symmetries of an arbitrary sample-only classification problem. Unit negative margins are valid for this unrestricted finite domain, not for arbitrary shared-rule grammars.

Four tests passed: target/restriction embeddings, exact checker on a valid and false fixture, sample/serialization validation, and input-symmetry normalization of a known full-domain circuit. No formally checked UNSAT proof trace or Lean theorem is claimed; replayable exact SMT instances and full normalizations are saved. A startup logging-helper bug was fixed and affected runs rerun before using results. All task-owned jobs finished and unrelated processes were preserved.


## 17. Focused paper revision completed

At the user's request, `workspace/threshold_paper/paper.tex` and `paper.pdf` now contain the strongest general exact upper bound and the useful improved average-case upper bounds with self-contained proofs and raw gate counts. The manuscript is19 pages, up from18. It deliberately excludes finite SMT records, exploratory coefficient languages, failed routes and the pending-review average-case lower-range extension. The unrelated modular-address proof sketch was removed to keep the revision focused; its earlier source remains in repository history.

The exact theorem states the finite bottom upper bound

$$\frac{N(N-1)}2+\frac{kN(m+\alpha)}2+2(N-1)+2\alpha k+3km+\left\lceil\frac{km}{2}\right\rceil,\qquad \alpha=\lfloor(m-1)/2\rfloor,$$

plus one top gate. Its proof gives an explicit score, the exceptional-address sign margins, affine raw-input expansion of every bottom gate, merged override gates and polynomial integer weights. At exact balance total size is $5n^2/16-(n/4)\log_2(n/2)+O(n)$; at floor balance it is $(5/16+o(1))n^2$. The earlier3n^2/4 construction is retained as a shorter introductory proposition and correctly identified as the merged Lean result.

The approximation theorem now gives $O(n^{3/2}\sqrt{\log(1/\delta)})$ gates for error delta and $O(\varepsilon^2n^{3/2}\sqrt{\log(1/\varepsilon)})$ gates (one extra n factor for support wires) over the stated small-advantage regime. Its full independent-mask, cross-moment, tail-second-moment and tie-handling proof is included. Fixed masks are chosen by a nonuniform averaging argument; efficient uniform mask selection is not claimed.

The abstract, result table, technique overview, remaining-gap statement and formalization section are synchronized. PRs2377,2813,2814 were rechecked as MERGED and2816 as OPEN. The new exact and approximation refinements are clearly NOT Lean formalized. A positive-part correction handles the sign-coherent entropy bound's trivial negative-numerator regime.

`verify_upper_updates.py` independently expands the new exact raw-gate score and checks58264 exhaustive table/block-count cases for k1..3,m1..4, plus larger spot checks up to k8,m32. Because the exact construction is block-uniform, these count checks cover every raw arrangement in those small instances. The same script exactly checks truncated staircase expansions and vanishing mixed-mask cross moments. Results are in `upper_update_checks.json`. `layout_checks.json` records19 pages, no missing/duplicate labels, no overfull boxes, no missing glyphs or undefined references, and visual inspection of the revised result pages. Universal proofs remain mathematical proofs rather than finite-test inference.

See `workspace/threshold_paper/REVISION.md` for the concise revision scope and build/check commands. All new authorship headers credit Christian Reitwiessner.


## 18. Completed coherence referee and one-table-bit lower bound

The Astra referee has now completed its review; this section supersedes the earlier in-progress description of `review_coherence`. The one-table-bit and extractor snapshots remain unfinished historical captures.

The drift lemma is valid under its exact **global** weight-comparability hypothesis. The repaired structural result controls only eligible blocks; it does not supersede the arbitrary-weight mixed-sign hybrid. The simultaneous marginal-entropy barrier is valid, but its purported universal limitation on all per-gate methods is not. Proposition 5.1 is false as stated because attainable values can have gaps.

The review proves a table-pair reduction for the one-table-bit class:

$$S\ge\frac N4\operatorname{slice}(m)=\Omega\!\left(\frac{Nm^{13/19}}{\log^{32/19}m}\right)=\widetilde\Omega(n^{32/19})$$

at balance. Here `slice(m)` is the minimum number of hyperplanes slicing every edge of the m-dimensional cube. This uses the known Sauermann–Xu slicing theorem ([arXiv:2510.16592](https://arxiv.org/abs/2510.16592)); it is a consequence for a restricted circuit class, **not** an improved unrestricted Andreev lower bound. No novelty priority for the corollary is claimed. For at most t table bits per bottom gate, the same accounting loses a factor t.

Proof idea: compare the actual top scores on two single-one tables whose indices differ in one address bit, and fix the other blocks. Their difference sign-represents m-bit parity. Gates reading neither table bit and all raw address terms cancel. Each surviving gate gives two halfspaces, which must collectively slice every edge. Sum over disjoint pairs of table labels. The final report supplies tie handling, hypotheses, counterexamples, and references.

The final referee report and both independent checking scripts are archived in `experiments/review_coherence/`. The parent reran `transfer_checks.py`: all exact checks passed (1,252 reflection-edge cases, 8,184 raw A1 inputs, 2,046 difference-parity inputs, 1,600 random cancellation cases). These checks support the algebra; the asymptotic theorem rests on the written reduction and cited slicing theorem. No shared manuscript was changed.
