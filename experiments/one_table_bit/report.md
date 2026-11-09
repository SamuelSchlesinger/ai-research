<!-- Copyright (c) 2026 Christian Reitwiessner. All rights reserved. -->
Authors: Christian Reitwiessner

# One-table-bit threshold circuits for ordinary Andreev

Research continuation, 2026-11-09. Work directory: `/tmp/andreev_gap/one_table_bit/`.
This report is saved incrementally. Labels distinguish **PROVED** (a hand proof supplied here), **COMPUTATION**, **REFUTED**, and **OPEN**. No independent referee review or Lean formalization is claimed. Existing mathematical attribution is retained below. No shared paper is edited.

## 1. Model and source audit

Put $N=2^k$, $D=km$, and $n=N+D$. There are independent table bits $x_c$, $c\in\{0,1\}^k$, and address bits $a\in\{0,1\}^D$. The label $b(a)$ consists of the $k$ block parities, and the target is $x_{b(a)}$. A bottom gate reads at most one table bit:

$$g_j(x,a)=[L_j(a)+\beta_jx_{c_j}\ge\theta_j].$$

Address weights and all top coefficients are arbitrary reals. Address-only bottoms and raw address/table inputs at the top are allowed. $S$ counts bottoms; add one for the output gate. Balanced means $D=N$ (on the integral subsequence where this is possible), or $D\asymp N$ for asymptotic comparisons.

Read: the supplied `RESEARCH_STATE.md`, `threshold_paper/paper.tex`, and the reports in `coherence_fable`, `push_lower`, `review_lower`, `upper_astra`, and `push_upper`. `review_coherence/report.md` was absent on initial inspection. In particular, claims from `coherence_fable` are not treated as independently reviewed results.

The unrestricted $5n^2/16+o(n^2)$ construction does not automatically give an upper bound in this subclass: its main ridges read many independent table bits. Its transfer must be proved, rather than inferred from its final score being affine in the table.

## 2. Exact correctness condition [PROVED]

For a fixed address, write the actual top score in bit coordinates as

$$F(x,a)=C(a)+\sum_c w_c(a)x_c.$$

This is always possible, since a function of the single bit $x_c$ is affine. More explicitly, let $h_{j,t}(a)=[L_j(a)+\beta_jt\ge\theta_j]$, $t\in\{0,1\}$. Then

$$w_c(a)=u_c+\sum_{j:c_j=c}v_j(h_{j,1}(a)-h_{j,0}(a)),$$

and $C$ includes the top constant, raw address term, address-only gates, and $\sum_jv_jh_{j,0}$. The difference $h_{j,1}-h_{j,0}$ is a signed indicator of a slab between parallel halfspaces. In terms of $q=\theta_j-L_j(a)$ it is active precisely when

$$\min(0,\beta_j)<q\le\max(0,\beta_j).$$

For the convention $[F\ge0]$, exact correctness at $a$, with $b=b(a)$, is equivalent to

$$C+\sum_{c\ne b}w_c^+<0\le C+w_b+\sum_{c\ne b}w_c^-,$$

where $w^+=\max(w,0)$ and $w^-=\min(w,0)$. These are the maximum negative-class score and minimum positive-class score, respectively. Thus the permitted intercept interval is

$$-w_b-\sum_{c\ne b}w_c^-\ \le C\ <\ -\sum_{c\ne b}w_c^+.$$

It is nonempty if and only if $w_b>\sum_{c\ne b}|w_c|$. This verifies the algebra in `coherence_fable`, Proposition 6.1, but makes its qualification “together with the matching value of $c(a)$” essential. Dominance alone is not sufficient for a given circuit: $F=2x_b+1$ satisfies dominance but outputs the constant one.

Equivalently, put $\xi_c=2x_c-1$, $K_c=w_c/2$, and $R=C+\frac12\sum_cw_c$. Then

$$F=R+\sum_c\xi_cK_c.$$

Let $A=K_b-\sum_{c\ne b}|K_c|$. The exact condition is

$$A>0,\qquad -A\le R<A.$$

If a strict margin is desired, a single sufficiently small downward shift of the top threshold score makes every correct finite circuit strict: all negative scores were already strictly negative, and all positive scores were nonnegative. After such a shift the condition is $A>|R|$. The odd-in-table dictionary model from `upper_astra`, Section 4, has $R=0$, and its stated strict dominance condition is exactly necessary and sufficient.

### Constant-factor equivalence with pure selector kernels [PROVED]

Given any correct one-table-bit circuit, replace its score by

$$F(x,a)-F(\mathbf1-x,a)=\sum_c w_c(a)(2x_c-1).$$

Both evaluations have opposite target labels, so their difference has the correct strict sign. Each complemented bottom still reads just one table bit. Address-only gates and raw address terms cancel; at most twice as many table-reading bottoms remain. Thus intercept repair costs at most a factor two, and the pure dominance formulation loses no gate exponent.

Conversely, a kernel expressed as a constant plus signed slabs can be multiplied by its own table sign with at most four ordinary one-table-bit bottom gates per slab: expand the slab as two halfspaces, and for each halfspace $E$ use $\xi_cE=2x_cE-E$. The conjunction $x_cE$ is an actual raw-input LTF by a sufficiently large table coefficient. Address-only $E$ gates can be shared. This establishes equivalence up to constant factors with the minimum total number of slab terms in a dominating family; it does not bound coefficient magnitudes.

## 3. Research status

Further bounds, obstructions, and computations will be appended after their proofs are checked. The targets remain an exponent above $3/2$ for the lower bound or an exact construction near $n^{3/2}$.
