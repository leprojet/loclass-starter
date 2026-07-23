# Changelog

## [0.3.0] - 2026-07-23

### Added

- Standalone end-user document template under `template/`.
- Document-local runner for PDF, ODT, diagnostics, and cleanup.
- Generation of LaTeX metadata and package resources from the LDL manifest.

### Changed

- Newly created documents no longer depend on `uv` or neighboring development
  repositories.
- Repository development files, examples, tests, and Git metadata are no longer
  copied into end-user documents.

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project follows Semantic
Versioning.

## [0.2.0] - 2026-07-18

### Added

- Integration of generated loclass package declarations into the LaTeX
  preamble.
- Managed LaTeX resource directory for package-owned TeX files.
- Pre-build preparation through `loclass latex prepare`.

### Changed

- The LaTeX build now aborts immediately when a preparation or conversion
  command fails.
- Existing `TEXINPUTS` values are preserved.
- Generated package declarations are loaded before project-specific
  preamble files.

## [0.1.0] - 2026-07-11

### Added

- Reference project structure for loclass documents.
- Complete modular LDL example document.
- Project-specific LaTeX templates and assets.
- PDF build workflow using the central loclass LaTeX backend.
- Direct ODT conversion through the central loclass CLI.
- Project diagnostics through `./loclass doctor`.
- Project configuration support.
- Development, build, formatting, and release-check commands.
- Examples for metadata, chapters, sections, paragraphs, lists, tables,
  images, code blocks, shell blocks, and inline elements.

### Changed

- Migrated LDL parsing and loading to `loclass-ldl`.
- Migrated conversion and rendering to `loclass-base`.
- Replaced the local formatter with `loclass format`.
- Renamed the PDF build helper to `build_ldl_pdf.py`.
- Consolidated the project frontend into the root `loclass` command.
- Reduced the starter repository to project workflow, templates, examples,
  configuration, and assets.

### Removed

- Duplicate LDL parser and document model.
- Duplicate LaTeX backend.
- Legacy `loclass-render` command.
- Duplicate `core/tools/loclass.lua` frontend.
- Compatibility facades for the previous architecture.
- Obsolete `Raw` examples and handling.
