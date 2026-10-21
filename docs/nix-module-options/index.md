---
title: 'Nix Module Options Explorer'
description: 'Query upstream NixOS and Home Manager module options offline with `nix eval` — existence checks, full option docs, and category listings, in any flake (overlay-aware pkgs with flake-parts debug mode).'
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

The expressions must run from inside your flake repository (they use `builtins.getFlake (builtins.toString ./.)`) and need **nix** and **jq**. Two backends are supported, selected automatically by a detection command:

- **Any flake** with a `nixpkgs` input (plus `home-manager` for HM queries) works via the fallback backend, which instantiates `pkgs` from `flake.inputs.nixpkgs` directly.
- **flake-parts flakes with `debug = true;`** get Backend A: it reuses the pre-evaluated, overlay-aware `pkgs` from `currentSystem.allModuleArgs`. Measured at the same speed as the fallback (the module-tree merge dominates both) — choose it for overlay-awareness. Without `debug = true;` that output doesn't exist — see the skill's troubleshooting for the (slightly surprising) fix involving committing the change.

## How it works

1. Detects whether the flake-parts debug output is available (`... ? currentSystem`), then picks the matching backend.
2. Both backends expose the same names — `lib`, `hmLib`, `hmOpts`, `nixosOpts` — so the query catalog is identical either way. Nix's laziness means only the queried option tree is evaluated.
3. Evaluates only **upstream modules** (imported directly from `${flake.inputs.home-manager}/modules/modules.nix` or `${flake.inputs.nixpkgs}/nixos/modules/module-list.nix`), so results reflect what NixOS/Home Manager actually ship — your custom modules are excluded by design.
4. Pipes the evaluated options through `jq` for readable output: `select(.visible == true)` hides internal options, and `.declarations` points at the upstream source file.
5. Batches multi-query tasks through a single `nix repl` session (the skill's Session Mode): each `nix eval` spawn re-pays the module-tree merge, so one session with many queries is ~3× faster than repeated spawns (~30ms per additional query).

Note the first query evaluates the entire upstream option tree — seconds warm, much longer cold; batch several queries into one `nix repl` session rather than re-paying that merge per `nix eval` (Nix's eval cache never serves values to `nix eval`). For heavy recurring use, the skill shows how to materialize the docs once as a derivation (`lib.nixosOptionsDoc` / `lib.hmOptionsDoc`) that the build cache does persist. For quick approximate lookups where the pinned revision doesn't matter, instant channel-snapshot sources exist (home-manager-options.extranix.com static JSON, search.nixos.org options API) — but they reflect channels, not your lockfile. To query your own configuration instead (including custom modules), evaluate `homeConfigurations.USERNAME.options.OPTION.PATH` directly.

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
