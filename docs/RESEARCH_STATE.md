<!-- Copyright (c) 2026 Christian Reitwiessner. All rights reserved. -->
Authors: Christian Reitwiessner

# Research state

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

### New coarse-Fourier family, fixed $k=3$

`experiments/mixed_upper_sol/report.md` and `constructions.py` give, for every $m\ge1$,

$$S_3(m)=6\lfloor m/2\rfloor+6m+\lfloor3m/2\rfloor+26$$

bottoms plus one top. This has slope $21/2$ and improves an inherited fixed-$k=3$ slope $27/2$. It does **not** improve the growing-$k$, balanced quadratic constant.

The new idea is sign-only reconstruction from coarse Walsh amplitudes. Put $h_S(x)=\sum_c\chi_S(c)x_c$ and $H_{S,r}=[h_S\ge r]$. Use thresholds $r=0,1$ for the six singleton/pair characters and $r=0$ for the triple: 13 amplitudes. Set $a_S=18$ for pairs and $15$ otherwise, and $D(x)=6(x_0+x_7)+8\sum_{c\ne0,7}x_c-30$. Then

$$F(x,b)=D(x)+\sum_{(S,r)}a_S\chi_S(b)(2H_{S,r}(x)-1)$$

satisfies $(2x_b-1)F\ge15$ on all 2048 table/address pairs, checked with integers. Gates $[6t_S+h_S\ge12j+r]$, together with table-only $H$, realize each product for every $m$. The report proves the identity and gives explicit weights/counts. These gates are **block-symmetric/sign-coherent**. The user now permits pursuing this direction only via genuinely mixed in-block signs toward subquadratic size.

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

The local paper PDF's formalization-status section predates some merges. Consult the above states and pinned code, rather than treating its old 'open PR' labels as current. The $5n^2/16$ research construction, coherent lower bounds, latest fixed-$k=3$ coarse Fourier family, and majority refinements are separate research artifacts; check their own evidence before claiming Lean coverage.

## 6. Completed mixed-sign coarse-Fourier search

`experiments/coarse_mixed_general/report.md` gives an exact localized coarse-product identity with mixed signs inside every active block. A window costs its retained integer layers plus two endpoints and has no uncancelled linear tail. A varying-width mask identity cancels arrangement dependence exactly; saved rational witnesses and checks establish this finite subproblem. These witnesses are more expensive than the existing full ladders.

The report also proves an exponential mask-support obstruction for exact reconstruction by translates of a single middle-layer kernel. This is restricted to that architecture, not an impossibility theorem for mixed threshold circuits or variable-width pooling. No subquadratic ordinary-Andreev construction was found. Efficient pooling across growing-k characters remains unresolved. All associated jobs finished before archival.
