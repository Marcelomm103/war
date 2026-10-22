import json
import subprocess
import sys
from pathlib import Path

from war_game_engine.contracts import contract_json_schema, parse_contract_json
from war_game_engine.versioning import CURRENT_VERSION_VECTOR

ROOT = Path(__file__).resolve().parents[1]


def test_engine_schema_matches_generated_frontend_types() -> None:
    schema_path = (
        ROOT
        / "lib"
        / "war_game_engine"
        / "src"
        / "war_game_engine"
        / "schemas"
        / "contract-envelope-v1.json"
    )
    types_path = (
        ROOT / "lib" / "war_analyzer" / "pwa" / "src" / "contracts.generated.ts"
    )

    assert json.loads(schema_path.read_text(encoding="utf-8")) == contract_json_schema()
    generated_types = types_path.read_text(encoding="utf-8")
    for name in (
        "ContractEnvelope",
        "PolicyManifest",
        "ReplayManifest",
        "DatasetManifest",
        "InferenceConfig",
        "SemanticVersionVector",
        "CertificateManifest",
    ):
        assert f"export interface {name}" in generated_types
    assert "action_encoding_version" in generated_types
    assert "observation_encoding_version" in generated_types


def test_public_example_is_decoded_by_the_engine_contract() -> None:
    example_path = (
        ROOT
        / "lib"
        / "war_game_engine"
        / "tests"
        / "fixtures"
        / "contracts"
        / "public_game_state.json"
    )
    envelope = parse_contract_json(example_path.read_text(encoding="utf-8"))

    assert envelope.api_version == "1.0.0"
    assert envelope.schema_version == "1.0"
    assert envelope.payload.contract_type == "public_game_state"
    assert CURRENT_VERSION_VECTOR.api_version == envelope.api_version


def test_ai_import_is_headless_in_the_aggregate_environment() -> None:
    script = (
        "import importlib, sys; "
        "assert importlib.import_module('war_ai').__name__ == 'war_ai'; "
        "tracking = importlib.import_module('war_ai.reproducibility'); "
        "assert tracking.RunManifest.__name__ == 'RunManifest'; "
        "assert 'war_game_engine' not in sys.modules; "
        "importlib.import_module('war_game_engine.contracts'); "
        "assert 'torch' not in sys.modules; "
        "assert 'cv2' not in sys.modules"
    )
    subprocess.run([sys.executable, "-c", script], check=True)
