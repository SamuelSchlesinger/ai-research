# Independent adversarial review of coherence_fable

Authors: Christian Reitwiessner

Date: 2026-11-09. Reviewer: Astra; independent work, without subagents.

Scope: ordinary $A_{k,m}$, $N=2^k$ independent table bits, $k$ parity-address blocks of $m$ raw bits, arbitrary real threshold weights, direct raw top inputs allowed. $S$ counts bottom gates. The asymptotic balanced regime means $km=\Theta(N)$; literal $km=N$ with integral equal blocks exists only on a subsequence (e.g. $k$ a power of two). No claim below needs equality beyond constant factors. No shared paper was edited and nothing was posted online.

Sources read: `/tmp/andreev_gap/coherence_fable/report.md` and its scripts/logs; `mixed_sign/report.md`, `review_lower/report.md`, and the requested `research_backup/docs/RESEARCH_STATE.md` and `threshold_paper/paper.tex`. Original source labels such as PROVED are not evidence of correctness. This report is saved incrementally. **PROOF** denotes an argument checked here; **COMPUTATION** denotes a finite check, not an asymptotic proof; **REFUTATION** is an explicit contradiction; **CONJECTURE/UNRESOLVED** is not a theorem.

## 1. Drift Lemma 4.1 — correct asymptotically under its actual hypotheses

**Verdict: CORRECT for the stated global-comparability hypothesis and random restriction; FIXABLE presentation issues in exact constants and interpretations.** Independent adversarial computations are recorded separately below once completed.

Write $G=\max_{i,l}|\gamma_{i,l}|>0$. The required block $i$ satisfies

$$G/W\le |\gamma_{i,l}|\le G\quad\text{for EVERY }l,\qquad \delta=|\sum_l\gamma_{i,l}|/(mG)\ge2/m.$$

This excludes zeros in that block, not just small nonzero coefficients. $G$ is the maximum across **all address blocks**. A block with local max/min ratio $W$ whose whole scale is much smaller than another block is not covered. For the structural conclusion $W$ must be fixed (or explicitly at most $n^{o(1)}$); its polynomial growth cannot be suppressed in $n^{-\varepsilon+o(1)}$. There is no restriction on table coefficients because the result is uniform in the fixed table and hence in the resulting threshold.

**PROOF (independent reconstruction).** Choose independent uniform permutations in the blocks and a uniform cube $c\in\{0,\ldots,m-1\}^k$. Conditional on live coordinate $\ell$ in block $i$, $c_i$ remains uniform and its preceding set $F$ is uniform among sets of that size. For every particular $T\subseteq[m]\setminus\{\ell\}$,

$$\Pr(F=T\mid\ell)=\frac1{m\binom{m-1}{|T|}}=\int_0^1q^{|T|}(1-q)^{m-1-|T|}\,dq.$$

Thus the beta-mixture representation is exact: draw $q\sim U[0,1]$, then include each nonlive bit independently with probability $q$. It is not a uniform raw-address restriction and is not valid for a fixed adversarial arrangement.

Condition on the other blocks and $\ell$. Splitting is the event $\Phi_q\in J$ for a half-open interval $J$ of length $R\le kG$, with $\Phi_q=\sum_{l\ne\ell}\gamma_{i,l}\xi_l$. Its drift $D'=\sum_{l\ne\ell}\gamma_{i,l}$ has $|D'|\ge\delta mG-G\ge\delta mG/2$; reflect signs if needed. Kolmogorov–Rogozin at scale $G/(2W)$, followed by a cover of $J$, gives

$$\Pr(\Phi_q\in J)\le\frac{C(2kW+1)}{\sqrt{(m-1)\min(q,1-q)}}.$$

Bernstein's inequality gives probability at most $2/m$ whenever $\operatorname{dist}(qD',J)\ge u(q)$, with

$$u(q)=2G\sqrt{(m-1)q(1-q)\ln m}+2G\ln m.$$

The remaining set $Q$ is contained in

$$|q-q_0|<a+b\sqrt{q(1-q)},\qquad a\le\frac{2(k+2\ln m)}{\delta m},\quad b\le\frac{4\sqrt{\ln m}}{\delta\sqrt m}.$$

Here is a simpler endpoint-safe justification of the integration step. On $q\le1/2$, put $r=\sqrt q$. All admissible $r$ satisfy $|r^2-q_0|<a+br$. For any two such points $r>s$, subtraction implies

$$(r-s-b)(r+s)<2a.$$

Since $r+s\ge r-s$, their diameter is at most $b+\sqrt{2a}$. Consequently $\int_{Q\cap[0,1/2]}q^{-1/2}\,dq\le2b+2\sqrt{2a}$. Use $r=\sqrt{1-q}$ for the other half. This also handles $q_0$ outside $[0,1]$; no invalid square root of a negative quadratic discriminant is needed. Integrating yields

$$p(g)\le O\!\left(\frac{kW}{m}\left[\frac{\sqrt{\ln m}}{\delta}+\sqrt{\frac{k+\ln m}{\delta}}\right]\right)+\frac2m.$$

This is the claimed asymptotic drift bound. The displayed numerical coefficient $8C_{KR}$ in the source is not derived literally by its stated substitutions (an additional $\sqrt2$ is then said to be absorbed into a supposedly fixed constant); use an unspecified absolute constant. This is irrelevant to the requested exponent question.

**Interpretation limits.** In the balanced regime $k=\Theta(\log n)$ this is $\widetilde O(k/(\delta m))$ for bounded $W$. With unrestricted growing $k$, the explicit $\sqrt{k/\delta}$ term must not be hidden in polylogarithmic notation. The bound is an upper bound, not a universal asymptotic equality: thresholds far outside the attainable range yield zero splitting, and zero drift does not force random-walk-like behavior. The source's $\Theta(\sqrt{k/m})$ statements describe particular signed-weight examples, not all gates. The drift lemma says nothing nontrivial when its upper bound exceeds one and says nothing at $\delta=0$.

**REFUTATION of replacing global comparability by local comparability.** Take two blocks: all $+1$ in the first, exactly half $+M$ and half $-M$ in the second, with $M>m+1$, and threshold $m+1/2$. The first block has local ratio one and local relative drift one. Nevertheless a random edge in the second block crosses between levels $0$ and $M$ with probability $\Theta(m^{-1/2})$ (the expected local time of a uniform balanced bridge); whenever it does, the whole cube splits regardless of the first prefix count. Thus local drift in the first block does not imply $\widetilde O(1/m)$ splitting. The stated lemma avoids this counterexample precisely because the first block does not have scale comparable to the global maximum.

## 2. Theorem 4.2 — a valid restricted hybrid consequence, not a universal zero-sum theorem

**Verdict: FIXABLE GAP in the derivation; CORRECT with the precise eligible-block quantifier below. The unrestricted zero-sum interpretation is WRONG.**

A block is **eligible at $W$** precisely when all its $m$ coefficients have magnitudes in $[G/W,G]$, with $G$ the gate's global address maximum. Non-drifting means

$$\forall i\text{ eligible at }W:\quad |\sum_l\gamma_{i,l}|<\delta_0mG.$$

It does NOT mean every block with bounded *local* max/min ratio. It does NOT imply that every block is eligible, or even that any block is eligible. A gate with a zero in every block, or with one very large and many much smaller coefficients in each block, can be non-drifting vacuously even when its signed sums are large relative to its local $\ell_1$ masses. The all-zero address case is inert and should be removed. Being outside the drifting class is not equivalent to being a random-walk gate.

**PROOF (repaired demand and table-reading conclusion).** Let $J$ index table-reading gates and $T_c=\sum_{j\in J}p_j^c$, where $p_j^c$ is actual nonconstancy probability over the uniform table on cube $c$. The corrected entropy theorem (reviewed in §3 below) and concavity of binary entropy imply

$$N-\log_2(N+1)\le\sum_{j\in J}[h(p_j^c)+kp_j^c]
\le S h(T_c/S)+kT_c
\le T_c\log_2(eS/T_c)+kT_c.$$

For $S\le N^2$ and sufficiently large $N=2^k$, this forces $T_c\ge N/(4k)$: when $T_c\le1$ the right side is only $O(k)$; when $T_c>1$ it is at most $(3k+\log_2 e)T_c$. Thus averaging over independent uniform arrangements and cubes gives

$$\sum_{j\in J}p_j\ge N/(4k).$$

This is the missing step. Entropy is not bounded pointwise by $k$ times the probability of splitting: the activity indicator itself can carry $h(p)$ bits. Nor does entropy directly prove the source's literal $N/(3k)$ bound without lower-order corrections. Pure-address gates contribute zero entropy even if they split, so doing the averaging over $J$ is essential to the claimed **table-reading** conclusion.

In the balanced regime Lemma 4.1 gives a uniform bound

$$p_j\le \frac{C k^{3/2}W\sqrt{\ln m}}{\delta_0m}+2/m$$

for drifting gates; coherent gates have $p_j\le k/m$. Choose a sufficiently large absolute $K$ and

$$\delta_0=Kk^{5/2}W\sqrt{\ln m}\,\frac{S}{Nm}.$$

Use the known unrestricted $\widetilde\Omega(N^{3/2})$ size lower bound to ensure $\delta_0\ge2/m$, or simply replace $\delta_0$ by its maximum with $2/m$ and handle that case explicitly. For $S\le N^{2-\varepsilon}$ and fixed $W$, $\delta_0=o(1)$ and the aggregate split mass of drifting table-reading gates is at most $N/(16k)+2S/m$ after increasing $K$. The coherent mass is at most $Sk/m=o(N/k)$. Hence a constant fraction of the required $N/k$ mass comes from gates in $J$ that are BOTH noncoherent and non-drifting. The independent arbitrary-weight survival bound from `mixed_sign` Lemma 3.1 is $p_j\le k/m+O(k^{3/2}/\sqrt m)$. Therefore there are

$$\Omega(N\sqrt m/k^{5/2})=\widetilde\Omega(n^{3/2})$$

such table-reading gates. Using the upper bound on $S$ gives $\delta_0\le N^{-\varepsilon}\operatorname{polylog}(N)W$, and for $S=\widetilde O(N^{3/2})$ it gives $\delta_0mG=\widetilde O(\sqrt m)G$. These are valid only on eligible blocks. The input research state records a separate improved $O(k/\sqrt m)$ survival proof; importing it could improve logs, not the exponent, and is unnecessary here.

**Does this supersede the previous mixed-sign hybrid? No, not as an unrestricted structural theorem.** `mixed_sign` Theorem 3.2 applies to arbitrary magnitudes, controls minority count, and forces a large noncoherent population. The new drift estimate distinguishes many gates that that run-count estimate treats poorly (e.g. fixed signed bias with a linear minority count). On an eligible block, near-zero signed sum is genuinely stronger: if $\mu$ is its minority count, then

$$\mu\ge m\frac{1-W\delta_0}{W+1},$$

by lower-bounding majority mass by $(m-\mu)G/W$ and upper-bounding minority mass by $\mu G$. This yields $\Omega(m)$ minority bits for fixed $W$ and small $\delta_0$. But on noneligible blocks there is no conclusion. The arbitrary-weight minority/run/sign-pattern statements therefore remain necessary. One can combine both charging bounds to force many gates outside the union of the small-minority and drifting classes; that is an additional hybrid argument, not supplied by the source's zero-sum slogan.

**Does it imply the coherent lower bound for unrestricted circuits? No.** It identifies exceptional gates with a permissible $\widetilde O(m^{-1/2})$ split rate and demands only $\widetilde\Omega(n^{3/2})$ of them. It neither converts them to coherent gates nor supplies a $\widetilde O(1/m)$ usefulness bound. It proves a near-quadratic result for a restricted class in which every gate is coherent or has an eligible block of definite drift. The general near-quadratic lower bound remains open. No asymptotic exponent improvement for unrestricted ordinary Andreev follows.

**Further quantifier error in source §5.4.** An aggregate demand for each arrangement, $\forall\sigma\,\sum_j p_j(\sigma)\ge D$, does not give a fixed set of gates each useful under EVERY arrangement. The gates supplying the demand can vary with $\sigma$. Similarly, Littlewood–Offord's upper bound on activity of table-heavy gates does not by itself force the same $\widetilde\Omega(n^{3/2})$ gates to have a specified small number of large table coefficients. A threshold on useful activity and another hybrid/counting step would be needed. Statements (3) and (4) of that four-property list are not established as stated.
