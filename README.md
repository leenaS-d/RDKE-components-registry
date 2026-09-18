# Core RDK Entertainment Platform Reference

A self-contained static reference site and generator for RDKE. All inputs,
scripts, styles, assets, and generated pages live in this directory.

## Generate pages

Run from the `RDKE` directory:

```python
python build.py
```

Import any API workbook directly by providing its output and column mappings:

```python
python import_apis.py Southbound-apis.xlsx southbound-apis.json --map halInterface="HAL interface" --map repo="Repo name" --map source=Source
```

The build writes the home page, Core RDK Components page, northbound API page,
southbound API page, and hardware specifications page. Individual generators
are also available:

```python
python gen_base_page.py
python gen_component_registry_page.py
python gen_nbi_page.py
python gen_sbi_page.py
python gen_hwcompat_page.py
```

`build.py` uses only the Python standard library. Use `python build.py --check`
to validate the local JSON inputs and generated page presence.

The API pages are generated from `Northbound-apis.xlsx` and
`Southbound-apis.xlsx` when the workbooks are present. The generic converter
maps each workbook into its corresponding JSON file before the page is rendered.
Southbound workbooks use `HAL interface`, `Repo name`, and `Source`; Northbound
workbooks use `Component`, `API`, `Description`, and `Reference`.

## Data files

- [components.json](components.json) - Core RDK component registry data.
- [northbound-apis.json](northbound-apis.json) - Generated Northbound API data.
- [southbound-apis.json](southbound-apis.json) - Generated Southbound API data.
- [Southbound-apis.xlsx](Southbound-apis.xlsx) - Southbound API source workbook.
- `Northbound-apis.xlsx` - Expected Northbound API source workbook in this repository.
- [hardware-spec.json](hardware-spec.json) - Extracted hardware specification data.
- [hardware-specifications.html](hardware-specifications.html) - Rendered hardware specification page.

Northbound and Southbound API source data is expected as Excel workbooks in this
repository. The hardware specification source is expected as a PDF named
`hardware-spec.pdf`; the build extracts it into [hardware-spec.json](hardware-spec.json).

## Hardware Spec PDF extraction

Place the hardware specification PDF at `hardware-spec.pdf`. The normal build
will extract its text and tables into `hardware-spec.json`, then render the
extracted content in `hardware-specifications.html`:

