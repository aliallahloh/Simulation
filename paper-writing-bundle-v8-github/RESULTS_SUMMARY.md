# Results Summary

## 1. Hybrid twin

The hybrid twin is strongest on load calibration.

Twin calibration highlights:
- validation load MAE: physics_only 41.55 vs hybrid_twin 7.11
- test load MAE: physics_only 92.70 vs hybrid_twin 10.43
- for PV, the hybrid twin is not universally better than the physics-only baseline on the test split

## 2. Forecasting

ALL-site load results:
- hybrid_personalized: MAE 15.69, RMSE 21.94, coverage_80 0.730
- federated_personalized: MAE 15.90, RMSE 22.20, coverage_80 0.739
- local_rich: MAE 20.29, RMSE 27.05, coverage_80 0.630
- centralized_rich: MAE 20.31, RMSE 27.92, coverage_80 0.689

ALL-site PV results:
- local_rich: MAE 2.37, RMSE 4.51, coverage_80 0.797
- federated_personalized: MAE 2.50, RMSE 4.98, coverage_80 0.788
- hybrid_personalized: MAE 2.56, RMSE 5.11, coverage_80 0.771
- centralized_rich: MAE 2.81, RMSE 5.55, coverage_80 0.793

Interpretation:
- personalized hybrid and federated models materially outperform the global-only variants
- the personalized load models are the strongest forecasting story in the full run
- calibration is good enough to support a trustworthy forecasting narrative, but not perfect

## 3. Full-run controller results

Trust-aware MPC beats deterministic MPC on operating cost under all stressed scenarios in the full run.

Cost deltas, trust-aware minus deterministic:
- baseline: -431.29 USD
- comm_loss_light: -573.71 USD
- comm_loss_heavy: -779.81 USD
- missing_meter_data: -1645.74 USD
- sensor_spike_anomalies: -2067.42 USD
- forecast_shock_pv_drop: -368.91 USD
- ev_surge_event: -368.95 USD
- compound_stress: -2028.89 USD

Peak-import deltas, trust-aware minus deterministic:
- baseline: +3.24 kW
- comm_loss_light: +3.24 kW
- comm_loss_heavy: +25.14 kW
- missing_meter_data: -115.31 kW
- sensor_spike_anomalies: -42.06 kW
- forecast_shock_pv_drop: -16.00 kW
- ev_surge_event: -4.81 kW
- compound_stress: -7.45 kW

Interpretation:
- the strongest control story is lower operating cost under abnormal scenarios
- peak-import gains are present but generally modest and not universal
- trust-aware control often uses materially more battery throughput, so that tradeoff must be discussed honestly

## 4. Ablation interpretation

The ablation evidence is meaningful but mixed.

Clear findings:
- removing the penalty term usually worsens cost relative to the full trust-aware controller
- fallback is no longer the sole driver of the trust-aware result in V8
- uncertainty effects are mixed rather than universally favorable

Therefore, the paper should claim:
- trust-aware scheduling and penalty-aware operation matter
- uncertainty modeling contributes but does not help uniformly in every stressed regime
