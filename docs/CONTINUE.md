<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Continuing the research

Read RESEARCH_STATE.md first. The primary objective is a smaller exact THR∘THR construction for ordinary Andreev, ultimately below quadratic size. Prioritize construction discovery over formalization; Lean verification can follow later.

## Current work

The earlier majority, small-instance SMT, mixed-sign upper-bound, and coarse-Fourier tasks have finished. Their reports are in `experiments/maj_sol`, `variants_sol`, `mixed_upper_sol`, and `coarse_mixed_general`. No old solver process needs resuming. The last report gives an exact localized mixed-sign product gadget, a varying-width cancellation identity, and a restricted obstruction for one middle-layer architecture. It obtains no subquadratic family. Pooling across growing-k characters is open.

The user now requests a fresh SMT search for larger k and m, with the generator encoding specified below. A background GPT Sol task is being started after this initial archive is pushed. Its future output is not part of this snapshot. Preserve new code, witnesses, results, and logs in a new experiment directory, then update this archive.

## The generator-SMT encoding: the essential quantifiers

Fix a finite Boolean gate basis and a size bound r for a k-input, one-output generator circuit. A description D specifies its gates and wiring. A fixed evaluator computes G_D(c). The table supplied to the candidate threshold circuit is

$$X(D)=(G_D(c))_{c\in\{0,1\}^k}.$$

The synthesis problem is

$$\exists\theta\ \forall D,a:\quad
\operatorname{Valid}_r(D)\Longrightarrow
T_\theta(X(D),a)=G_D(b(a)).$$

Here b(a) is the vector of address-block parities. The same threshold parameters θ must work for every valid generator description and address. The threshold circuit receives **evaluated table bits**, never D, generator gate values, or a description-dependent choice of weights. Universal descriptions are represented by finitely many symbolic bits and a universal evaluator, not higher-order quantification.

Use counterexample-guided synthesis: a learner finds θ on concrete evaluated tables and addresses; a checker fixes θ and searches existentially for valid D and a violating the equality. A SAT checker model supplies a new concrete example. An UNSAT checker certifies correctness on the declared generator family. A timeout or UNKNOWN certifies nothing. Record the family, basis, size convention, and validity rules.

Restricting descriptions restricts the table family unless coverage of all tables is proved. Family correctness alone is not an ordinary-Andreev upper bound. When a promising candidate is found, check it independently against arbitrary raw table bits and addresses. Reusing identical evaluated tables is allowed. Retaining all 2^k evaluated inputs also retains that many possible weights per bottom gate: generator encoding does not automatically shrink the synthesis parameter count.

Avoid the incorrect alternatives ∃D choosing an easy generator, ∀D∃θ giving a different circuit for each table, or feeding description bits to T. All three change the problem.

## Useful implementation starting points

- `workspace/smt_symbolic_check.py`: arbitrary-table symbolic miter, avoiding full truth-table enumeration. It is not itself the generator encoding.
- `experiments/mixed_sign/mscore.py`: existing real-weight learner and circuit conventions.
- `experiments/variants_sol`: earlier CEGIS experiments and failed candidates.
- `experiments/mixed_upper_sol`: exact construction certificates and ten-bottom A_(2,3)/A_(2,4) witnesses.

The top threshold may read the raw table and address inputs as well as bottom outputs; count S bottoms and S+1 total gates. Use exact rational/integer checking for any reported witness. A bounded integer-weight UNSAT result is only about that weight bound. Keep gate counts separate from coefficient multiplicity and wire counts.

Use increasing bounded budgets and persist progress promptly. Start with modest generator sizes and larger k,m; compare alternative targets with baselines before long runs. Aim for a useful SAT construction rather than prolonged attempts to prove small sizes impossible. Negative finite searches do not settle an asymptotic upper bound.

## User preferences

- Credit new files to **Christian Reitwiessner**. Preserve original contributors and mathematical citations in archived files.
- Use dollar-delimited mathematics in explanations.
- Use GPT Sol for the SMT work and for unfinished tasks that hit another provider's rate limit.
- Seek clever upper bounds. The user mostly trusts research proofs and intends Lean verification later.
- For the coarse-Fourier direction, require genuinely different mixed signs *inside* relevant blocks across gates. Merely giving different blocks uniform signs or applying one common input reorientation is not the requested direction.
- Keep proved results, exact finite checks, heuristic candidates, UNKNOWN, and conjectures distinct.

## Reproduction and updating

`tools/verify_archive.py` checks preserved file hashes. `tools/run_experiment.py` makes a writable staged copy and translates old absolute paths there; inspect scripts before running expensive searches. Dependencies are recorded, not vendored. Original logs and witnesses are retained verbatim, including obsolete claims; consult the curated summary for corrections.

After a new completed experiment, copy its whole directory into `experiments/`, update the curated notes, regenerate MANIFEST.json, run the integrity checker, and commit/push. Do not include installed dependencies, credentials, caches, or transient work copies. The original chat is not required to interpret the mathematical state in this archive.
