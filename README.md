<p align="center">
  <img src="assets/images/banner.png" alt="loclass – Write here • Read everywhere" width="100%">
</p>

# loclass-starter

`loclass-starter` is a reference project and practical starting point for
structured technical documentation with **loclass** and the
**loclass document language (LDL)**.

It contains a complete example document, project assets, LaTeX integration,
and a small project frontend for common development and build tasks.

## Role in the loclass ecosystem

The loclass ecosystem is split into three repositories:

| Repository | Purpose |
| --- | --- |
| `loclass-ldl` | LDL specification, parsing, loading, formatting, and document model |
| `loclass-base` | Conversion pipeline, CLI, and output backends |
| `loclass-starter` | Reference project and starter structure for loclass documents |

The processing flow is:

```text
LDL source
    ↓
loclass-ldl
    ↓
neutral Document model
    ↓
loclass-base converter
    ↓
LaTeX or ODT
    ↓
project-specific build workflow
```

`loclass-starter` does not contain its own LDL parser or rendering backend.
Those responsibilities belong to `loclass-ldl` and `loclass-base`.

## Repository contents

The starter project provides:

- an example LDL document
- modular document content through `input`
- project-specific assets and images
- LaTeX templates and configuration
- PDF generation through the loclass LaTeX backend
- direct ODT conversion through the central loclass CLI
- project configuration
- development and diagnostic commands
- a reference directory structure for new documentation projects

## Current LDL features

The example project demonstrates:

- document metadata
- chapters and sections
- paragraphs
- inline elements
- lists
- tables
- code blocks
- shell blocks
- images and captions
- modular source files through `input`
- LaTeX and ODT output

Supported inline elements include:

```ldl
__cmd{uv run pytest}
__keys{Ctrl+Alt+T}
__url{https://example.org/docs}
__code{None}
```

## Quick start

Install the dependencies:

```bash
uv sync
```

Inspect the project environment:

```bash
./loclass doctor
```

Build the configured document:

```bash
./loclass build
```

Build the full LDL example as PDF:

```bash
./loclass ldl examples/full_document.ldl
```

Convert the example directly to ODT:

```bash
uv run loclass convert \
  examples/full_document.ldl \
  --backend odt \
  --output build/full_document.odt
```

The generated files are written to the `build/` directory.

## LDL example

A root LDL file begins with one manifest followed by document content:

```ldl
---
title: LDL Example Document
subtitle: Built directly from LDL
author: Frank Sieger
company: LogObject
customer: Example Customer
language: en
theme: default
version: 0.1.0
revision: 1
date: 2026-07-09
---

input
  content/chapter-one.ldl

Run the tests with __cmd{uv run pytest}.

Press __keys{Ctrl+Alt+T}.

Further information is available at __url{https://example.org/docs}.

The return value is __code{None}.
```

An included file contains document content only:

```ldl
chapter
  Introduction

This is an LDL document.

section
  Execution

The configuration is stored in __code{/etc/nginx/nginx.conf}.
```

## LDL `input`

The `input` directive composes a document from multiple LDL source files:

```ldl
input
  content/chapter-one.ldl
```

Rules:

- paths are resolved relative to the file containing the directive
- included files contain document content only
- the manifest belongs exclusively to the root document
- a document has exactly one manifest
- missing files produce readable errors
- circular includes are detected and rejected

Example:

```text
examples/
├── full_document.ldl
└── content/
    └── chapter-one.ldl
```

Source composition is handled by `loclass-ldl` before an output backend is
invoked.

## Project structure

```text
.
├── assets/
│   └── images/
├── content/
├── core/
│   └── tools/
├── examples/
│   └── content/
├── project/
├── build/
├── dev
├── loclass
├── main.tex
├── latexmkrc
├── pyproject.toml
└── README.md
```

The exact contents may evolve, but the separation remains:

- `content/` contains project document sources
- `assets/` contains images and other document assets
- `project/` contains project-level configuration
- `core/tools/` contains starter-specific build helpers
- `build/` contains generated output

## Development checks

Run the project diagnostics:

```bash
./loclass doctor
```

Run Python tests:

```bash
uv run pytest
```

Run static checks:

```bash
uv run ruff check core
uv run ruff format --check core
```

Check LDL formatting:

```bash
uv run loclass format examples/full_document.ldl --check
```

## Design principles

- Document content remains separate from output formatting.
- LDL parsing is provided by `loclass-ldl`.
- Conversion and output backends are provided by `loclass-base`.
- The starter contains only project-specific workflow and assets.
- Generated files remain outside the source structure.
- A starter project should be understandable, reproducible, and easy to copy.

## Version

The current development milestone is `0.1.0`.
