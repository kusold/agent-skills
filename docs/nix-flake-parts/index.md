---
title: 'Nix Flake-Parts — Modular Flake Framework'
description: 'Expert guidance for the flake-parts framework: convert flakes to mkFlake, organize modular configurations, master perSystem, module arguments, easyOverlay, and reusable flakeModules.'
weight: 60
---

Expert guidance for [flake-parts](https://flake.parts), the framework that applies the NixOS module system to flake organization. The skill helps you convert standard flakes to `flake-parts.lib.mkFlake`, organize configurations into importable modules, and eliminate the `forAllSystems` boilerplate that multi-system flakes usually require.

**Use when:**

- "Convert my flake to flake-parts"
- "Organize my flake into modules"
- "How do perSystem and flake differ?"
- "Use `inputs'` instead of `inputs.packages.${system}`"
- "Create a reusable flakeModule"
- "Generate an overlay from perSystem packages"
- Debugging flake-parts evaluation errors, circular dependencies, or missing module arguments

**Covers:**

- Converting standard `outputs = { ... }: { packages = forAllSystems ... }` flakes to `mkFlake` with a `systems` list
- `perSystem` vs `flake`: which outputs belong per-system (packages, devShells, apps, checks, formatter) and which are unique (nixosConfigurations, homeConfigurations)
- Module arguments: `pkgs`, `system`, `config`, `inputs'` and `self'` (system pre-selected), `final` (with easyOverlay), plus top-level `withSystem`, `getSystem`, and `moduleWithSystem`
- The `@` pattern bound on the outer module for accessing top-level and per-system `config` without shadowing
- `moduleWithSystem` for exporting NixOS modules that use packages from the defining flake
- `importApply` for passing flake-level context (like `withSystem`) into imported modules
- The `easyOverlay` flakeModule — imported at the **top level** of your mkFlake module — and the `final` vs `pkgs` distinction
- Exporting reusable `flakeModules` for other flakes to consume
- Debugging with `debug = true` and `nix repl` inspection
- Migration validation: `nix flake check --no-build` for fast eval-only iteration between steps, full `nix flake check --all-systems` (or `nix-fast-build` in CI) for final checks

## Key concepts

The core benefit of flake-parts: define a package once in `perSystem` and it is automatically generated for every system in your `systems` list — `packages.hello` becomes `packages.x86_64-linux.hello`, `packages.aarch64-linux.hello`, and so on, without `genAttrs` plumbing.

Compared with `eachSystem`-style helpers (flake-utils), flake-parts transposes per-system outputs lazily — requesting one attribute evaluates only that system. On a full `nix flake check` (8 systems) that measured 3.2× faster than the eager fold-merge, and each consumer avoids adding its own helper entry to the lock file; for point evaluations the two are equally fast.

Two ideas trip up most newcomers, and the skill gives both special attention:

- **Named arguments only.** The module system inspects your function signature with `builtins.functionArgs`; only parameters you explicitly name (`{ pkgs, system, config, ... }`) receive values. A catch-all `args:` gets none of the special arguments.
- **`final` vs `pkgs` under easyOverlay.** `pkgs` is the package set *before* your overlay, `final` is the set *after*. When packages reference each other, use `final` so they pick up the overlaid versions instead of the originals.

The skill also covers flake-parts gotchas: files must be git-tracked before the flake can see them ("path does not exist" errors), `self` must not be accessed directly in modules (inside `perSystem`, use `self'` or `config`; from flake level, use `withSystem`), and inputs should never be traversed with `mapAttrs`.

## Usage

Invoke the skill by name, or let a supporting agent select it for a relevant request. Automatic activation depends on the host agent and its configuration.

**Examples:**

```
Convert my flake to flake-parts with support for x86_64-linux and aarch64-linux
```
```
Refactor this devShell to use inputs' instead of inputs.packages.${system}
```
```
Create an overlay from my perSystem packages
```

## Installation

```bash
npx skills add kusold/agent-skills --skill nix-flake-parts
```

Or install all skills from this repository with `npx skills add kusold/agent-skills`.

## Going deeper

Four focused guides ship alongside the skill definition, loaded on demand when the task needs more than the essentials:

- [module-arguments.md](../../skills/nix-flake-parts/module-arguments.md) — complete reference for every module argument, the `@` pattern, and function signature inspection
- [overlays.md](../../skills/nix-flake-parts/overlays.md) — easyOverlay in depth: selective `overlayAttrs`, the `final` vs `pkgs` distinction, and common pitfalls
- [modular-organization.md](../../skills/nix-flake-parts/modular-organization.md) — `importApply` patterns, reusable `flakeModules`, dogfooding, and module file structures
- [advanced.md](../../skills/nix-flake-parts/advanced.md) — partitions, custom flake outputs, debug mode, `allSystems`, and migration from standard flakes

If your goal is the specific architecture where *every* file (except entry points like `flake.nix`) is a top-level flake-parts module, see the companion [nix-dendritic-flake](../nix-dendritic-flake/) skill. To query what options upstream NixOS or Home Manager modules expose, see [nix-module-options](../nix-module-options/).

## Full Skill Reference

See [skills/nix-flake-parts/SKILL.md](../../skills/nix-flake-parts/SKILL.md) for the complete guide (mkFlake structure, perSystem options, module arguments, conversion with safety guardrails, best practices, debugging, and common issues, with pointers to the four focused guides) that the agent loads when this skill is active.
