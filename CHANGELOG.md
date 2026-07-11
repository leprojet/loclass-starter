# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project follows Semantic
Versioning.

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
