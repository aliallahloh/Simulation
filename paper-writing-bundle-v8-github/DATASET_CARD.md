# Dataset Card

## Dataset identity

This GitHub-safe bundle packages the benchmark metadata and the validated full-run evidence needed to draft the paper.

## Full local benchmark used by the experiment

The underlying experiment used these core benchmark files locally:
- `dataset_core/aligned/aligned_vpp_benchmark_long.csv`
- `dataset_core/expanded/expanded_federated_benchmark_long.csv`
- `dataset_core/overlays/battery/battery_assets.csv`
- `dataset_core/scenarios/trust_scenarios.csv`

This GitHub folder includes the battery metadata plus the compact evidence tables needed for writing.

## Study setting

The benchmark represents a renewable-rich, grid-interactive VPP/microgrid-style testbed with:
- multiple site types
- battery overlays
- EV demand overlays
- scenario overlays for trust and stress
- aligned and expanded client-style datasets for local, centralized, federated, and hybrid learning

## Intended use

This package is intended for:
- paper drafting
- results narration
- methods reporting
- table and figure planning
- limitation framing

It is **not** intended for inventing unsupported claims.

## Full-run split

The full configuration used:
- train end: 2018-08-31 23:45:00
- validation end: 2018-10-31 23:45:00
- test end: 2018-12-31 23:45:00

## Full-run scenarios

- baseline
- comm_loss_light
- comm_loss_heavy
- missing_meter_data
- sensor_spike_anomalies
- forecast_shock_pv_drop
- ev_surge_event
- compound_stress

## Controllers in the final comparison

- `rule_based`
- `deterministic_mpc`
- `trust_aware_mpc`

## Forecast model families in the final comparison

- `local_rich`
- `centralized_rich`
- `federated_personalized`
- `hybrid_personalized`

## Important limitations

The final paper should state clearly:
- trust-aware gains are strongest on **cost/resilience**, not on dramatic peak reduction
- uncertainty ablations are mixed rather than universally favorable
- trust-aware improvements often come with materially higher battery throughput
- the hybrid twin is strongest on **load**; do not claim universal twin dominance for PV
