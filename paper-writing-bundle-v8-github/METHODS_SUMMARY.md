# Methods Summary

## Final validated branch

This bundle corresponds to the validated V8 package branch: a hybrid-twin, personalized federated forecasting, and trust-aware risk-scheduled MPC stack.

## Pipeline structure

1. Data ingestion
   - aligned benchmark time series
   - expanded federated-style client data
   - battery asset metadata
   - trust/stress scenarios

2. Hybrid digital twin
   - physics-style site/hour baselines for load and PV
   - residual correction model
   - twin diagnostics and anomaly-oriented outputs

3. Forecasting
   - gradient-boosted tree forecasters using XGBoost hist trees
   - richer features: short lags, anchor lags, rolling statistics, cyclical time, battery/EV/price/weather interactions
   - model families:
     - local_rich
     - centralized_rich
     - federated_personalized
     - hybrid_personalized
   - global-only ablations:
     - federated_global_only
     - hybrid_global_only

4. Trust-aware dispatch
   - rule-based baseline
   - deterministic MPC baseline
   - trust-aware risk-scheduled MPC
   - V8 controller rewrite introduced:
     - risk-scheduled LP
     - soft reserve slack
     - soft peak slack
     - terminal shortfall slack
     - emergency-only fallback rather than fallback-dominated behavior

5. Stress testing
   - the controller is evaluated under multiple abnormal operational scenarios, especially missing data, anomaly spikes, communication loss, PV shock, EV surge, and compound stress

## Safe claim boundary

Safe claims:
- personalized hybrid/federated forecasting materially outperforms global-only variants
- the hybrid twin strongly improves load-state calibration relative to the physics-only twin
- trust-aware dispatch reduces operating cost under abnormal conditions
- the integrated stack is more operationally robust under abnormal conditions than deterministic MPC alone

Claims to avoid:
- deep MARL or unconstrained RL performance
- universally superior uncertainty-module effect
- universally lower peak demand in every scenario
- full battery-health optimization beyond throughput observations

## Exact full-run highlights

- forecast estimators: 50
- max depth: 6
- learning rate: 0.05
- dispatch horizon: 32 steps at 0.25 hours
- stress scenarios: baseline, communication loss, missing data, anomaly spikes, PV shock, EV surge, compound stress

See configs/full.yaml for the exact parameter values.
