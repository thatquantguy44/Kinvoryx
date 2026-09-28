# Home Sweet Home Source Check Runbook

This runbook covers the zero-dollar, read-only source benchmark for Spec 013.
It checks source availability and response shape only. It does not retain raw API
payloads, listing rows, addresses, household profiles or credentials.

## Local configuration

Use the tracked example as the template:

```sh
cp config/home_sweet_home.sources.example.yaml config/home_sweet_home.sources.local.yaml
chmod 600 config/home_sweet_home.sources.local.yaml
```

The local file is ignored by git through `config/*.local.yaml`. Store API keys
only in the local file.

## Run the metadata check

```sh
python3 scripts/home_sweet_home_source_check.py \
  --output /private/tmp/kinvoryx_home_sweet_home_source_check.json
```

The output file is a metadata report. It includes source IDs, endpoint families,
HTTP status, response shape, top-level JSON keys, optional result-count hints and
timing. It must not include secrets, raw responses, listings, household inputs or
exact private locations.

If Python reports certificate-chain failures, keep TLS verification enabled. The
source checker uses Certifi when available so Python can validate public HTTPS
services without disabling certificate checks.

## Current benchmark evidence

Last metadata-only run: September 27, 2026.

- Succeeded: 10 source probes.
- Warning: 1 source probe.
- Raw payloads retained: no.
- Output path used for local inspection: `/private/tmp/kinvoryx_home_sweet_home_source_check.json`.

Observed source statuses:

| Source ID | Status | Meaning |
|---|---|---|
| `trellistate_public_listings` | ok | Public listing endpoint responded, but the tiny DC query returned an empty sample. Coverage remains unproven. |
| `wmata_predictions_no_key` | warn | WMATA station-prediction endpoint returned HTTP 401 without a key. |
| `wmata_predictions_keyed` | ok | WMATA endpoint responded with the local portal key. |
| `usajobs_search` | ok | USAJOBS search responded with authenticated metadata. |
| `airnow_zip_observation` | ok | AirNow ZIP observation endpoint responded. |
| `noaa_cdo_datasets` | ok | NOAA CDO token and dataset catalog responded. |
| `nws_points` | ok | NWS no-key point metadata responded with the configured contact user-agent. |
| `openfema_disaster_declarations` | ok | OpenFEMA disaster-declaration endpoint responded. |
| `fema_nfhl_metadata` | ok | FEMA NFHL ArcGIS metadata responded. |
| `census_acs_profile` | ok | Census ACS profile endpoint responded. |
| `bls_public_series` | ok | BLS public time-series endpoint responded. |

## Fictional benchmark profiles

The first synthetic DC-area profile set is stored at
`data/home_sweet_home/dc_benchmark_profiles.json`. It contains fictional
profiles only and is intended to test whether source evidence can support:

- renter transit search with no school needs
- buyer search with education enabled
- two-adult competing commutes
- accessibility and transit reliance
- remote-work broadband and air-quality context
- childcare timing and mixed buy/rent comparison

These profiles are not real households and are not recommendations.
