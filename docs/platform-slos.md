# Platform SLOs (Developer-Centric)

These SLOs measure the internal developer experience provided by the framework and its tooling. Targets are initial and subject to refinement.

- SLO-PR-FEEDBACK-P95-15M: 95% of pull requests receive CI feedback (tests + lint) within 15 minutes.
- SLO-SAVE-SUCCESS-99_9: Monthly success rate for `chatlog save` ≥ 99.9%.
- SLO-SAVE-LATENCY-P95-200MS: 95th percentile latency from save invocation to index update < 200ms (local run).
- SLO-DOCS-BUILD-GREEN: Docs build passes on main 100% of the time; link-check has ≥ 99% pass rate.
- SLO-ONBOARD-15M: Time to install and run first successful `chatlog save` from a fresh clone ≤ 15 minutes (measured periodically).

Notes

- Measurement sources may be a combination of CI timings, local benchmarks, and periodic surveys.
- As capabilities evolve (centralized storage, telemetry), these SLOs should be refined and made more objective.
