# RDKE Platform Reference

A self-contained static reference site and generator for RDKE. All inputs,
scripts, styles, assets, and generated pages live in this directory.

## Generate pages

Run from the `RDKE` directory:

```powershell
python build.py
```

The build writes the home page, Core RDK Components page, northbound API page,
southbound API page, and hardware specifications page. Individual generators
are also available:

```powershell
python gen_base_page.py
python gen_component_registry_page.py
python gen_nbi_page.py
python gen_sbi_page.py
python gen_hwcompat_page.py
```

`build.py` uses only the Python standard library. Use `python build.py --check`
to validate the local JSON inputs and generated page presence.

## Generator design

The scripts are RDKE-specific adaptations of the source repository generators.
They do not import the parent repository's `layout.py`, PDF/XLSX extraction,
remote DML/HAL maps, or Core RDK Broadband navigation. This keeps RDKE portable
when it is moved into its own repository.

## Data files

- `home-content.json` - Home page copy, architecture cards, and RDK8 context.
- `components.json` - Core RDK component registry from the pinned
	`meta-rdk/docs/core-components/core-v-components.json` source.
- `northbound-apis.json` - Northbound API records, currently empty.
- `southbound-apis.json` - Southbound API records, currently empty.
- `hardware-spec.json` - Hardware profiles, currently empty.

The northbound and southbound specification pages are intentionally not
included yet. The API and hardware list pages are ready to be populated when
the Excel workbook and hardware profiles are provided.

## Hardware Spec PDF extraction

Place the hardware specification PDF at `hardware-spec.pdf`. The normal build
will extract its text and tables into `hardware-spec.json`, then render the
extracted content in `hardware-specifications.html`:

