---
title: 'Nix Dendritic Flake — flake-parts Conversion'
description: 'Convert Nix flakes to the dendritic pattern with flake-parts, where every file except entry points is a top-level module and shared options replace specialArgs.'
weight: 70
---

Convert Nix flakes to use [flake-parts](https://flake.parts) with the [dendritic pattern](https://github.com/mightyiam/dendritic), where every `.nix` file except entry points (`flake.nix`, `default.nix`) is a top-level flake-parts module. File paths name features (not types), NixOS/home-manager/nix-darwin configurations live as `deferredModule` option values, and modules share values through top-level `config` — eliminating `specialArgs` pass-through.

**Use when:**

- "Convert to dendritic"
- "Every file is a module"
- "Organize my nix config"
- "Replace specialArgs with shared options"
- Adopting dendritic architecture for NixOS, home-manager, or nix-darwin configurations

For general flake-parts mechanics (`perSystem`, overlays, module arguments), see the companion [nix-flake-parts](../nix-flake-parts/) skill - flake-parts literacy is a prerequisite for this conversion. To query what options upstream NixOS or Home Manager modules expose, see [nix-module-options](../nix-module-options/).

**Covers:**

- Restructuring `flake.nix` around `mkFlake` with [import-tree](https://github.com/denful/import-tree) auto-importing
- Module directory layout: infrastructure (`systems.nix`, `meta.nix`, `nixos.nix`), features (`shell.nix`, `admin.nix`), hosts (`myhost.nix`)
- The `flake.modules.{nixos,darwin,homeManager}` pattern for cross-platform features
- Adding home-manager and nix-darwin infrastructure modules
- Replacing `specialArgs` with shared top-level options
- Migration checklist with tiered validation: `nix flake check --no-build` for quick eval-only checks, [nix-fast-build](https://github.com/Mic92/nix-fast-build) or a full check for real builds

## The conversion workflow

The skill walks through the migration in order: add `flake-parts` and `import-tree` inputs, convert `flake.nix` outputs to `mkFlake`, then build up the `modules/` tree — target systems, shared options in `meta.nix`, per-platform configuration infrastructure, and finally feature and host modules that import features via `flake.modules`. Deferred modules (`lib.types.deferredModule` with `lazyAttrsOf`) keep evaluation lazy, and the NixOS infrastructure module generates `flake.checks` for each NixOS configuration's toplevel — so a plain `nix flake check` builds every host closure, and `nix flake check --no-build` gives you eval-only validation of all hosts between migration steps.

Best practices the skill enforces: one feature per file, file paths as feature names, no `specialArgs`, declaring your own options to model the system (with `flake.modules` as the cross-platform convenience), and upstream's anti-patterns — no `enable`-option boilerplate, no module-name proliferation. Real-world reference migrations include [mightyiam/infra](https://github.com/mightyiam/infra), [vic/vix](https://github.com/vic/vix), and [drupol/nixos-x260](https://github.com/drupol/nixos-x260) — the closest thing to a step-by-step conversion walkthrough.

## Usage

Invoke the skill by name, or let a supporting agent select it for a relevant request. Automatic activation depends on the host agent and its configuration.

**Examples:**

```
Convert my NixOS flake to the dendritic pattern with flake-parts
```
```
Refactor my flake so every file is a top-level module
```
```
Organize my nix config into feature modules instead of host-specific specialArgs
```

## Installation

```bash
npx skills add kusold/agent-skills --skill nix-dendritic-flake
```

Or install all skills from this repository with `npx skills add kusold/agent-skills`.

## Full Skill Reference

See [skills/nix-dendritic-flake/SKILL.md](../../skills/nix-dendritic-flake/SKILL.md) for the complete guide (prerequisite inputs, before/after `flake.nix`, anti-patterns, condensed best practices, debugging, and the full migration checklist) that the agent loads when this skill is active. Two supporting references carry the full module walkthroughs: [infrastructure-modules.md](../../skills/nix-dendritic-flake/infrastructure-modules.md) (`systems.nix`, `meta.nix`, `nixos.nix`, home-manager and nix-darwin plumbing) and [feature-and-host-modules.md](../../skills/nix-dendritic-flake/feature-and-host-modules.md) (feature modules, host modules, the `flake.modules` pattern, `deferredModule` semantics, replacing `specialArgs`).
