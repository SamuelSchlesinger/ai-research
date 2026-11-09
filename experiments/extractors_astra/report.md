<!-- Copyright (c) 2026 Christian Reitwiessner. All rights reserved. -->
Authors: Christian Reitwiessner

# Extractors and depth-two threshold complexity of ordinary Andreev

Research cutoff: 2026-11-09. Work performed independently, without subagents. This report is being written incrementally. The source workspace is read-only; no shared paper is edited and nothing is posted online. Mathematical results retain their original attribution.

## 1. Scope and verified starting point

Write $N=2^k$, $b_i=\bigoplus_{j=1}^m a_{i,j}$, and $A(x,a)=x_b$, on $n=N+km$ bits. Exact balance means $km=N$; the integer constraint $k\mid 2^k$ matters, and other sizes use floor balance/padding. The circuit is $\mathrm{THR}\circ\mathrm{THR}$ with arbitrary real weights and direct raw-input wires into the top gate. Size below counts bottom gates, up to an additive one for the top. Uniform average case means uniform independent **table and raw address** bits. Advantage $\varepsilon$ means agreement $1/2+\varepsilon$; error $\delta$ means agreement $1-\delta$.

Read first: the requested `research_backup/docs/RESEARCH_STATE.md`, `threshold_paper/novelty_search.md`, `andreev_depth_two_bounds.md`, `kw_applications.md`, `kane_williams_erratum.md`, and relevant portions of `threshold_paper/paper.tex` in the source workspace. Earlier reports are historical, not necessarily current theorem statements.

**Baseline correction discovered on reading the current manuscript.** The latest `paper.tex`, theorem `thm:avgupper` and its proof (lines 486–610), already removes the union-bound $\sqrt{\log n}$ loss for fixed error:

$$S_{1-\delta}=O\!\left(n^{3/2}\sqrt{\log(1/\delta)}\right),\qquad 0<\delta\le 1/2.$$

It also proves

$$S_{1/2+\varepsilon}=O\!\left(\varepsilon^2 n^{3/2}\sqrt{\log(1/\varepsilon)}\right),\qquad N^{-1/2}\le\varepsilon\le1/8.$$

These are inherited results, not findings of this investigation. The proof uses independent address masks and a second-moment error estimate; the masks are fixed nonuniformly by averaging. Exact computation has the inherited $5n^2/16+o(n^2)$ upper bound. The inherited unrestricted lower bounds are $\Omega(\varepsilon^2n^{3/2}/\log^2n)$ gates and $\Omega(\varepsilon^2n^{5/2}/\log^{5/2}n)$ support wires, in the proved common range $\varepsilon\ge3(k+2)/\sqrt N$. Pending hand proofs extending the gate advantage range must not be confused with formalized results. The coherent $\Omega(n^2/\log^3n)$ bound restricts within-block signs and is not an unrestricted bound.

## 2. Evidence and status discipline

The requested primary source is Kane–Williams, [arXiv:1511.07860v1](https://arxiv.org/pdf/1511.07860), dated 24 November 2015. Its ordinary function, its code-based $B_n$, and later extractor-based generalized functions will be kept distinct. Local errata describe proof repairs and an advantage-range gap; quoting the original abstract alone is insufficient.

Subsequent sections will distinguish **proved deductions in this report**, **verified external theorems**, **conditional implications**, **refutations of specified routes**, and **unresolved possibilities**. No assertion that a literature search proves novelty or exhaustively establishes the latest result is intended.
