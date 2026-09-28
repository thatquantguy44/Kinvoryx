"""Source contracts and metadata-only checks for Home Sweet Home research."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
import ssl
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


PLACEHOLDER_MARKERS = ("replace_with_", "your_", "paste_")


@dataclass(frozen=True)
class SourcePolicy:
    """A source-level contract before any housing recommendation consumes data."""

    source_id: str
    capability: str
    endpoint_family: str
    cost_model: str
    requires_key: bool
    key_config_paths: tuple[str, ...] = ()
    no_key_allowed: bool = False
    output_grain: str = "unknown"
    raw_payload_retention_allowed: bool = False
    intended_use: str = ""
    limitation: str = ""

    def to_metadata(self) -> dict[str, Any]:
        data = asdict(self)
        data["key_config_paths"] = list(self.key_config_paths)
        return data


@dataclass(frozen=True)
class SourceCheckResult:
    """Metadata-only result for one read-only source probe."""

    source_id: str
    status: str
    checked_at_utc: str
    endpoint_family: str
    http_status: int | None = None
    elapsed_ms: int | None = None
    response_shape: str | None = None
    top_level_keys: list[str] = field(default_factory=list)
    result_count_hint: int | None = None
    raw_payload_retained: bool = False
    message: str = ""

    def to_metadata(self) -> dict[str, Any]:
        return asdict(self)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def nested_get(config: dict[str, Any], path: str) -> Any:
    value: Any = config
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def configured_secret(config: dict[str, Any], *paths: str) -> str | None:
    for path in paths:
        value = nested_get(config, path)
        if isinstance(value, str):
            stripped = value.strip()
            if stripped and not stripped.startswith(PLACEHOLDER_MARKERS):
                return stripped
    return None


def configured_text(config: dict[str, Any], path: str, default: str) -> str:
    value = nested_get(config, path)
    if isinstance(value, str) and value.strip() and not value.startswith(PLACEHOLDER_MARKERS):
        return value.strip()
    return default


def summarize_json_shape(payload: bytes) -> tuple[str, list[str], int | None]:
    try:
        parsed = json.loads(payload.decode("utf-8"))
    except Exception:
        return ("non_json", [], None)

    if isinstance(parsed, dict):
        keys = sorted(str(key) for key in parsed.keys())[:12]
        count: int | None = None
        for candidate in ("results", "features", "data", "items"):
            value = parsed.get(candidate)
            if isinstance(value, list):
                count = len(value)
                break
        if count is None and isinstance(parsed.get("resultset"), dict):
            count_value = parsed["resultset"].get("count")
            if isinstance(count_value, int):
                count = count_value
        return ("object", keys, count)
    if isinstance(parsed, list):
        return ("array", [], len(parsed))
    return (type(parsed).__name__, [], None)


def verified_ssl_context() -> ssl.SSLContext | None:
    try:
        import certifi  # type: ignore
    except Exception:
        return None
    return ssl.create_default_context(cafile=certifi.where())


def metadata_get(
    *,
    source_id: str,
    endpoint_family: str,
    url: str,
    headers: dict[str, str] | None = None,
    method: str = "GET",
    body: bytes | None = None,
    timeout_seconds: float = 12.0,
) -> SourceCheckResult:
    started = time.monotonic()
    request = Request(url, data=body, headers=headers or {}, method=method)
    ssl_context = verified_ssl_context()
    try:
        with urlopen(request, timeout=timeout_seconds, context=ssl_context) as response:
            payload = response.read(96_000)
            elapsed_ms = int((time.monotonic() - started) * 1000)
            shape, keys, count = summarize_json_shape(payload)
            return SourceCheckResult(
                source_id=source_id,
                status="ok",
                checked_at_utc=now_utc(),
                endpoint_family=endpoint_family,
                http_status=response.status,
                elapsed_ms=elapsed_ms,
                response_shape=shape,
                top_level_keys=keys,
                result_count_hint=count,
                message="metadata-only source probe succeeded",
            )
    except HTTPError as exc:
        elapsed_ms = int((time.monotonic() - started) * 1000)
        status = "warn" if exc.code in {401, 403, 404, 429} else "fail"
        return SourceCheckResult(
            source_id=source_id,
            status=status,
            checked_at_utc=now_utc(),
            endpoint_family=endpoint_family,
            http_status=exc.code,
            elapsed_ms=elapsed_ms,
            message=f"HTTP {exc.code}; no raw response retained",
        )
    except (TimeoutError, URLError, OSError) as exc:
        elapsed_ms = int((time.monotonic() - started) * 1000)
        return SourceCheckResult(
            source_id=source_id,
            status="fail",
            checked_at_utc=now_utc(),
            endpoint_family=endpoint_family,
            elapsed_ms=elapsed_ms,
            message=f"{type(exc).__name__}; no raw response retained",
        )


def skipped_result(source_id: str, endpoint_family: str, message: str) -> SourceCheckResult:
    return SourceCheckResult(
        source_id=source_id,
        status="skipped",
        checked_at_utc=now_utc(),
        endpoint_family=endpoint_family,
        message=message,
    )


def source_policies() -> dict[str, SourcePolicy]:
    policies = [
        SourcePolicy(
            source_id="trellistate_public_listings",
            capability="listing_probe",
            endpoint_family="trellistate_public_listing_search",
            cost_model="zero_dollar_public_read",
            requires_key=False,
            no_key_allowed=True,
            output_grain="listing_offer",
            intended_use="Tiny source-shape probe for public buy/rent listing reads.",
            limitation="Coverage is public/user-submitted and cannot establish active-listing completeness.",
        ),
        SourcePolicy(
            source_id="wmata_predictions_no_key",
            capability="transit_access",
            endpoint_family="wmata_station_predictions",
            cost_model="free",
            requires_key=False,
            no_key_allowed=True,
            output_grain="station_prediction",
            intended_use="Determine whether a WMATA endpoint responds without a portal key.",
            limitation="WMATA schedules/predictions are inputs to routing, not door-to-door trips.",
        ),
        SourcePolicy(
            source_id="wmata_predictions_keyed",
            capability="transit_access",
            endpoint_family="wmata_station_predictions",
            cost_model="free_keyed",
            requires_key=True,
            key_config_paths=("wmata.api_key", "wmata.secondary_api_key"),
            output_grain="station_prediction",
            intended_use="Verify the user-provided free WMATA portal key works where required.",
            limitation="A working key does not validate route accessibility or reliability.",
        ),
        SourcePolicy(
            source_id="usajobs_search",
            capability="active_federal_jobs",
            endpoint_family="usajobs_search",
            cost_model="free_keyed",
            requires_key=True,
            key_config_paths=("usajobs.authorization_key",),
            output_grain="job_announcement",
            intended_use="Small current federal-posting search for DC job-access evidence.",
            limitation="Federal announcements do not represent the whole labor market.",
        ),
        SourcePolicy(
            source_id="airnow_zip_observation",
            capability="air_quality",
            endpoint_family="airnow_zip_observation",
            cost_model="free_keyed",
            requires_key=True,
            key_config_paths=("airnow.api_key",),
            output_grain="monitor_observation",
            intended_use="Air quality and smoke context for source feasibility.",
            limitation="Observation data is not property-specific health or indoor-air advice.",
        ),
        SourcePolicy(
            source_id="noaa_cdo_datasets",
            capability="climate_context",
            endpoint_family="noaa_cdo_v2",
            cost_model="free_keyed",
            requires_key=True,
            key_config_paths=("noaa_cdo.token",),
            output_grain="dataset_catalog",
            intended_use="Verify NOAA CDO token and catalog shape.",
            limitation="Climate data requires station/location selection before address use.",
        ),
        SourcePolicy(
            source_id="nws_points",
            capability="weather_alerts_forecast",
            endpoint_family="nws_points",
            cost_model="free_no_key",
            requires_key=False,
            no_key_allowed=True,
            output_grain="forecast_grid_metadata",
            intended_use="No-key National Weather Service endpoint check with contact user-agent.",
            limitation="Weather forecast metadata is not a long-term hazard model.",
        ),
        SourcePolicy(
            source_id="openfema_disaster_declarations",
            capability="hazard_context",
            endpoint_family="openfema_api",
            cost_model="free_no_key",
            requires_key=False,
            no_key_allowed=True,
            output_grain="county_disaster_declaration",
            intended_use="Check public OpenFEMA disaster declaration API shape.",
            limitation="Disaster history is contextual and not property-level risk or insurance pricing.",
        ),
        SourcePolicy(
            source_id="fema_nfhl_metadata",
            capability="flood_hazard_context",
            endpoint_family="fema_nfhl_arcgis_rest",
            cost_model="free_no_key",
            requires_key=False,
            no_key_allowed=True,
            output_grain="flood_layer_metadata",
            intended_use="Check FEMA NFHL REST metadata availability.",
            limitation="Flood layer context is not a property inspection or insurance quote.",
        ),
        SourcePolicy(
            source_id="census_acs_profile",
            capability="area_context",
            endpoint_family="census_acs_profile",
            cost_model="free_key_optional",
            requires_key=False,
            key_config_paths=("census.api_key",),
            no_key_allowed=True,
            output_grain="county_profile",
            intended_use="Small ACS profile call for area housing context.",
            limitation="Area context cannot become demographic desirability scoring.",
        ),
        SourcePolicy(
            source_id="bls_public_series",
            capability="labor_market_context",
            endpoint_family="bls_public_api",
            cost_model="free_key_optional",
            requires_key=False,
            key_config_paths=("bls.registration_key",),
            no_key_allowed=True,
            output_grain="time_series",
            intended_use="Small BLS public time-series call for labor-market context.",
            limitation="Regional labor context is not a current opening or a hiring chance.",
        ),
    ]
    return {policy.source_id: policy for policy in policies}


def build_probe_definitions(config: dict[str, Any]) -> list[tuple[SourcePolicy, dict[str, Any]]]:
    policies = source_policies()
    definitions: list[tuple[SourcePolicy, dict[str, Any]]] = []

    definitions.append(
        (
            policies["trellistate_public_listings"],
            {
                "url": "https://trellistate.com/api/v1/listings?"
                + urlencode({"city": "Washington", "state": "DC", "limit": "1"}),
            },
        )
    )
    definitions.append(
        (
            policies["wmata_predictions_no_key"],
            {"url": "https://api.wmata.com/StationPrediction.svc/json/GetPrediction/A01"},
        )
    )
    wmata_key = configured_secret(config, "wmata.api_key", "wmata.secondary_api_key")
    definitions.append(
        (
            policies["wmata_predictions_keyed"],
            {
                "url": "https://api.wmata.com/StationPrediction.svc/json/GetPrediction/A01",
                "headers": {"api_key": wmata_key} if wmata_key else {},
                "skip_without": wmata_key,
                "missing_message": "WMATA key is not configured; no keyed endpoint probe run",
            },
        )
    )
    usajobs_key = configured_secret(config, "usajobs.authorization_key")
    usajobs_user_agent = configured_text(
        config,
        "usajobs.user_agent",
        "KinvoryxHomeSweetHome/0.1 source-check",
    )
    definitions.append(
        (
            policies["usajobs_search"],
            {
                "url": "https://data.usajobs.gov/api/search?"
                + urlencode({"LocationName": "Washington, DC", "ResultsPerPage": "1"}),
                "headers": {
                    "Host": "data.usajobs.gov",
                    "User-Agent": usajobs_user_agent,
                    "Authorization-Key": usajobs_key or "",
                },
                "skip_without": usajobs_key,
                "missing_message": "USAJOBS authorization key is not configured",
            },
        )
    )
    airnow_key = configured_secret(config, "airnow.api_key")
    definitions.append(
        (
            policies["airnow_zip_observation"],
            {
                "url": "https://www.airnowapi.org/aq/observation/zipCode/current/?"
                + urlencode(
                    {
                        "format": "application/json",
                        "zipCode": "20001",
                        "distance": "25",
                        "API_KEY": airnow_key or "",
                    }
                ),
                "skip_without": airnow_key,
                "missing_message": "AirNow API key is not configured",
            },
        )
    )
    noaa_token = configured_secret(config, "noaa_cdo.token")
    definitions.append(
        (
            policies["noaa_cdo_datasets"],
            {
                "url": "https://www.ncei.noaa.gov/cdo-web/api/v2/datasets?" + urlencode({"limit": "1"}),
                "headers": {"token": noaa_token or ""},
                "skip_without": noaa_token,
                "missing_message": "NOAA CDO token is not configured",
            },
        )
    )
    nws_agent = configured_text(
        config,
        "nws.contact_user_agent",
        "KinvoryxHomeSweetHome/0.1 source-check",
    )
    definitions.append(
        (
            policies["nws_points"],
            {
                "url": "https://api.weather.gov/points/38.9072,-77.0369",
                "headers": {"User-Agent": nws_agent, "Accept": "application/geo+json, application/json"},
            },
        )
    )
    definitions.append(
        (
            policies["openfema_disaster_declarations"],
            {
                "url": "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries?"
                + urlencode({"$filter": "state eq 'DC'", "$top": "1"}),
            },
        )
    )
    definitions.append(
        (
            policies["fema_nfhl_metadata"],
            {
                "url": "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer?"
                + urlencode({"f": "json"}),
            },
        )
    )
    census_key = configured_secret(config, "census.api_key")
    census_params = {
        "get": "NAME,DP04_0001E",
        "for": "county:001",
        "in": "state:11",
    }
    if census_key:
        census_params["key"] = census_key
    definitions.append(
        (
            policies["census_acs_profile"],
            {
                "url": "https://api.census.gov/data/2023/acs/acs5/profile?" + urlencode(census_params),
            },
        )
    )
    definitions.append(
        (
            policies["bls_public_series"],
            {
                "url": "https://api.bls.gov/publicAPI/v2/timeseries/data/LAUCN110010000000003?"
                + urlencode({"startyear": "2024", "endyear": "2024"}),
            },
        )
    )
    return definitions


def run_source_checks(config: dict[str, Any]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    policies = source_policies()

    for policy, probe in build_probe_definitions(config):
        if probe.get("skip_without") is None and "skip_without" in probe:
            result = skipped_result(
                policy.source_id,
                policy.endpoint_family,
                str(probe.get("missing_message", "required configuration is missing")),
            )
        else:
            result = metadata_get(
                source_id=policy.source_id,
                endpoint_family=policy.endpoint_family,
                url=str(probe["url"]),
                headers=probe.get("headers") or {},
                method=str(probe.get("method", "GET")),
                body=probe.get("body"),
            )
        results.append(result.to_metadata())

    return {
        "schema_version": 1,
        "generated_at_utc": now_utc(),
        "raw_payloads_retained": False,
        "scope": "metadata-only zero-dollar Home Sweet Home source benchmark",
        "policies": {key: policy.to_metadata() for key, policy in sorted(policies.items())},
        "results": results,
    }
