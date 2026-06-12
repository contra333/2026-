# Product

## Register

Academic conference poster.

## Users

Korean statistics conference reviewers, researchers, and attendees reading a
printed A0 portrait poster at varying distances. They need the research claim,
experimental setup, figures, and tables to be legible quickly while still
supporting closer technical inspection.

## Product Purpose

The primary product is a one-page A0 portrait TeX/PDF poster communicating that
ID accuracy alone is insufficient because optimizer/config choices can alter
calibration, feature geometry, and post-hoc OOD reliability.

## Current Poster Surface

The live source of truth is `poster/poster.tex`; the context summary is
`docs/research/current_poster_context.md`.

Current visible structure:

1. Figure 1: reliability failure concept.
2. Figure 2: validation-selected reliability scatter.
3. Figure 3: raw-vs-L2 near-OOD AUROC for one representative per optimizer.
4. Table 1: DDU-style GMM classwise covariance regularization.
5. Table 2: feature distribution geometry.
6. Conclusion and future work.

## Scholarly Voice

This is not a commercial brand surface. It should read as a careful statistical
argument: evidence-led, precise, and restrained. The poster may be visually
confident at distance, but the authority should come from clear hierarchy,
figures, tables, and explicitly bounded claims rather than brand expression.

## Design Principles

1. Distance-first hierarchy: title, section bars, figures, and tables must read
   before paragraphs.
2. Evidence over decoration: the composition should prioritize the current
   empirical figures and diagnostics, not ornamental panels.
3. One-page discipline: every block earns its space on the A0 portrait page.
4. Academic restraint: use strong alignment, spacing, and type hierarchy rather
   than visual novelty.

## Anti-References

Avoid marketing hero layouts, decorative gradients, floating blobs, nested
cards, rounded card-heavy compositions, ornamental visual effects, cramped
paragraphs, and palettes that drift away from the established poster blues.

## Accessibility

Use high contrast black text on white, strong section labels, generous line
spacing, and large enough type for printed poster reading. Do not rely on color
alone in tables or figures; captions and labels should remain explicit.
