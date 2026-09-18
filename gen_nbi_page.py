"""RDKE northbound API list generator."""
from build import build_api
from import_apis import convert_excel_to_json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def build_northbound() -> None:
    convert_excel_to_json(
        ROOT / "Northbound-apis.xlsx",
        ROOT / "northbound-apis.json",
        {
            "component": ("component", "service", "module"),
            "name": ("api", "api name", "interface"),
            "description": ("description", "details", "summary"),
            "reference": ("reference", "source", "url", "repo"),
        },
    )
    build_api(
        data_file="northbound-apis.json",
        output_file="northbound-apis.html",
        active="northbound",
        title="Northbound APIs",
        description="Standardized APIs the middleware exposes upward to the application layer, giving apps consistent access to device capabilities via Thunder and Firebolt.",
        columns=["Component", "API", "Description", "Reference"],
        fields=["component", "name", "description", "reference"],
        link_field="reference",
        search_placeholder="Search Northbound APIs",
        empty_message="No Northbound APIs have been loaded.",
        sort_field="component",
        draft_note="This page contains an evolving list of Northbound API components. The current list is a draft and will continue to be updated.",
    )

if __name__ == "__main__":
    build_northbound()
