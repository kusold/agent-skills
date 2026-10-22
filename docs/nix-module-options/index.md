---
title: 'Nix Module Options Explorer'
description: 'Query upstream NixOS and Home Manager module options from locked flake inputs with `nix eval` — existence checks, full option docs, and category listings, in any flake (overlay-aware pkgs with flake-parts debug mode).'
weight: 80
---

Query NixOS and Home Manager module options programmatically using flake evaluation — no web searches or option-search sites required. The skill provides ready-made `nix eval --impure` expressions that evaluate the upstream Home Manager and NixOS module systems from your flake's locked inputs, returning option existence, full documentation (type, description, default, examples, declarations), and category listings as JSON.

**Use when:**

- "Does Home Manager have a module for X?"
- "What options does `services.postgresql` have?"
- "Check NixOS options for Z"
- "Explore available options"
- "Get the docs / default / type for `programs.git.enable`"
- "What programs are available in Home Manager?"

**Queries covered:**

- Existence checks: is `OPTION.PATH` defined upstream? (`or null` + `--apply 'o: o != null'` — prints `true`/`false`)
- Full option documentation via `lib.optionAttrSetToDocList`
- Listing all options in a category (`builtins.attrNames`)
- Both module systems: Home Manager (`hmOpts`) and NixOS (`nixosOpts`)

## Requirements and compatibility

The expressions need **nix** and **jq**. Run them from your flake root, the directory containing `flake.nix`, because they use `builtins.getFlake (builtins.toString ./.)`. Two backends are supported, selected automatically by a detection command:

- **Any flake** with a `nixpkgs` input (plus `home-manager` for HM queries) works via the fallback backend, which instantiates `pkgs` from `flake.inputs.nixpkgs` directly.
- **flake-parts flakes with `debug = true;`** get Backend A: it reuses the pre-evaluated, overlay-aware `pkgs` from `currentSystem.allModuleArgs`. Choose it to reuse overlays. Without `debug = true;` that output doesn't exist — use Backend B when debug mode is absent. Edits to tracked files are visible without committing; newly created module files must be tracked.

## How it works

1. Detects whether the flake-parts debug output is available (`... ? currentSystem`), then picks the matching backend.
2. Both backends expose the same names — `lib`, `hmLib`, `hmOpts`, `nixosOpts` — so the query catalog is identical either way. Nix's laziness means only the queried option tree is evaluated.
3. Evaluates only **upstream modules** (imported directly from `${flake.inputs.home-manager}/modules/modules.nix` or `${flake.inputs.nixpkgs}/nixos/modules/module-list.nix`), so results reflect what NixOS/Home Manager actually ship — your custom modules are excluded by design.
4. Uses `nix eval --json` before piping the evaluated options through `jq` for readable output: `select(.visible == true)` hides internal options, and `.declarations` points at the upstream source file.
5. Batches related queries through a single `nix repl` session (the skill's Session Mode) to reuse the evaluated module tree.

Evaluation time depends on the inputs, cache state, and machine. Reuse one REPL session for related queries. Channel-based option search sites can support approximate lookups, but their results may differ from your lockfile. To query your own configuration (including custom modules), inspect `homeConfigurations.USERNAME.options` and project documentation fields before JSON serialization.

Inputs must already be available locally for offline use; Nix may otherwise fetch them. Dynamic submodule names such as nginx virtual hosts are documented through their option type, rather than indexed directly in the upstream option tree. Full documentation can force defaults that require user configuration; the skill explains how to project only needed fields before serialization.

## Usage

Invoke the skill by name, or let a supporting agent select it for a relevant request. Automatic activation depends on the host agent and its configuration.

**Examples:**

```
Does Home Manager have a duf module?
```
```
What options does programs.git have?
```
```
List the options in the services category for NixOS
```

## Installing

```bash
npx skills add kusold/agent-skills --skill nix-module-options
```

## Full Command Reference

See [skills/nix-module-options/SKILL.md](../../skills/nix-module-options/SKILL.md) for both backend expressions, the query catalog (existence checks, option docs, and category listings for Home Manager and NixOS), common option categories, documentation fields, and troubleshooting that the agent loads when this skill is active.
