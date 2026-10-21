---
name: nix-dendritic-flake
description: Convert Nix flakes to the dendritic pattern with flake-parts, where every file is a top-level module. Use when adopting dendritic architecture, restructuring NixOS/home-manager/nix-darwin configurations into feature-named modules, or replacing specialArgs with shared top-level options. Activates for queries like "convert to dendritic", "every file is a module", "organize my nix config", or "replace specialArgs with options". For general flake-parts mechanics (perSystem, overlays, module arguments), use the nix-flake-parts skill instead.
metadata:
  source: https://github.com/mightyiam/dendritic
---

# Dendritic Flake Conversion

Expert guidance for converting Nix flakes to the dendritic pattern with flake-parts - where every Nix file except entry points is a top-level module.

## What is the Dendritic Pattern?

The dendritic pattern uses a **top-level configuration** - commonly flake-parts, though it does not have to be (`lib.evalModules` directly also works) - where:
- **Every Nix file is a module** of the top-level configuration, except entry-point files such as `flake.nix` and `default.nix`
- Each file **implements a single feature** across all configurations it applies to
- File **paths name features**, not types or configuration classes
- Lower-level configs (NixOS, home-manager, nix-darwin) are stored as **option values** using `deferredModule` type

**Key benefit**: Files can share values via top-level `config`, eliminating `specialArgs` pass-through patterns.

**Evaluation cost** (measured): import-tree auto-import adds single-digit milliseconds per ~300 modules versus explicit imports, and both the options-instead-of-`specialArgs` switch and the `deferredModule` indirection are within measurement noise - the pattern's wins are architectural, and the real cost is evaluating the host configurations themselves (see tiered validation in the Migration Checklist).

## Anti-patterns

Mirrors the upstream project's guidance - keep these in mind when writing modules:

### `enable` options

`enable` options (often from `lib.mkEnableOption`) are only necessary when a module is imported even though the feature it provides should not necessarily be active. **In most cases, importing a module should enable the feature it provides** - do not generate `mkEnableOption` boilerplate by default.

### Not declaring options

Using only existing options (such as flake-parts' `flake.modules`) for the storage of lower-level modules prevents translating your mental model of the system into code. Declaring your own options is the primary modeling tool:

```nix
options.nixos.base = lib.mkOption { type = lib.types.deferredModule; };
```

Treat `flake.modules` as a convenience for cross-platform feature modules (see [feature-and-host-modules.md](feature-and-host-modules.md)), not as the only storage mechanism.

### Lower-level module name proliferation

If two lower-level modules are not distinct, do not invent a new name - merge them under one common name.

### Fanaticism

Exceptions are fine. A `my-package.pkg.nix` convention for callPackage-style files is acceptable, with such files excluded from auto-import.

## Prerequisites

Required flake inputs for dendritic setup:

```nix
{
  inputs = {
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
    import-tree.url = "github:denful/import-tree";  # Auto-imports all modules
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    # Optional: home-manager, nix-darwin, etc.
  };
}
```

`import-tree` auto-imports every `.nix` file under the module tree; paths containing `/_` are ignored by default.

## Conversion Steps

### Step 1: Restructure flake.nix

**Before (traditional):**
```nix
{
  outputs = { nixpkgs, ... }: {
    nixosConfigurations.myhost = nixpkgs.lib.nixosSystem {
      modules = [ ./hosts/myhost ./modules/common.nix ];
    };
  };
}
```

**After (dendritic):**
```nix
{
  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    import-tree.url = "github:denful/import-tree";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; }
      (inputs.import-tree ./modules);  # All modules auto-imported
}
```

### Step 2: Create Module Directory Structure

```
modules/
  systems.nix           # systems = [ "x86_64-linux" ... ]
  flake-parts.nix       # Import flake-parts extras (flakeModules.modules)
  meta.nix              # Top-level options (username, hostname, etc.)
  nixos.nix             # configurations.nixos option definition
  shell.nix             # Feature: shell config across platforms
  admin.nix             # Feature: admin/sudo across platforms
  myhost.nix            # Host: defines configurations.nixos.myhost
```

### Steps 3-6: Infrastructure, Features, and Hosts

Steps 3-4 - core infrastructure (`systems.nix`, `flake-parts.nix`, `meta.nix`, `nixos.nix`, plus home-manager and nix-darwin infrastructure modules) - are fully worked in [infrastructure-modules.md](infrastructure-modules.md).

Steps 5-6 - feature modules, host modules, the `flake.modules` pattern, and replacing `specialArgs` - are in [feature-and-host-modules.md](feature-and-host-modules.md).

## Migration Checklist

1. [ ] Commit or branch first - this is a wholesale restructure; start from a clean tree
2. [ ] Add `flake-parts` and `import-tree` inputs
3. [ ] Convert `flake.nix` to use `mkFlake` with `import-tree`
4. [ ] `git add -N modules/*.nix` as you create them - new files are invisible to flakes until git-tracked
5. [ ] Create `modules/systems.nix` with target systems
6. [ ] Create `modules/flake-parts.nix` importing `flakeModules.modules`
7. [ ] Create `modules/meta.nix` for shared options (move from `specialArgs`)
8. [ ] Create infrastructure modules (`nixos.nix`, `darwin.nix`, etc.)
9. [ ] Convert host configs to use `configurations.<class>.<name>.module`
10. [ ] Refactor shared code into feature modules using `flake.modules`
11. [ ] Remove `specialArgs` usage - use top-level options instead
12. [ ] Validate - quick pass: `nix flake check --no-build` (eval-only; still evaluates every generated check, catching option/merge errors across all hosts); full pass: `nix-fast-build` (parallel eval + build of `.#checks`, remote-capable) or a plain `nix flake check` in CI

## Best Practices

1. **One feature per file** - Each file implements a single, named feature
2. **File paths are feature names** - `modules/docker.nix` = docker feature
3. **Declare options to model your system** - Own `options.* = lib.mkOption { type = lib.types.deferredModule; }` is the primary tool; `flake.modules.{nixos,darwin,homeManager}.featureName` is the built-in convenience for cross-platform features
4. **No specialArgs** - Declare shared values as top-level options
5. **Lazy evaluation** - Use `lib.types.lazyAttrsOf` for configuration options
6. **Generate checks, validate in tiers** - Build `flake.checks` from configuration toplevels (see `nixos.nix` in [infrastructure-modules.md](infrastructure-modules.md)). This creates one check per host's toplevel, so a plain `nix flake check` builds every host closure - use `nix flake check --no-build` for eval-only validation while iterating, and [nix-fast-build](https://github.com/Mic92/nix-fast-build) (or a full check in CI) when you want the builds. Determinate Nix >= 3.16.3 parallelizes `nix flake check` by default.

## Debugging

Enable debug mode first - the `debug` flake output only exists when this is set:

```nix
{
  debug = true;
  # ... rest of config
}
```

Commit the change (or `git add -N`), then inspect with `nix repl`:

```bash
nix repl
:lf .
debug.allSystems.x86_64-linux           # Inspect a specific system
currentSystem.allModuleArgs.pkgs        # Inspect evaluated pkgs
currentSystem.options.<option>.files    # See where values are defined
debug.options.systems.declarations      # See where options are declared
```

Uncommitted changes are invisible to `:lf .` - it reads the git tree.

## Real-World Examples

- [mightyiam/infra](https://github.com/mightyiam/infra) - Original adoption
- [vic/vix](https://github.com/vic/vix) - Extensive example
- [drupol/nixos-x260](https://github.com/drupol/nixos-x260) - Well-documented migration; the closest thing to a step-by-step conversion walkthrough

## Related Skills

- **nix-flake-parts** - General flake-parts mechanics (`perSystem`, overlays, module arguments, debugging); flake-parts literacy is a prerequisite for this conversion

## References

- [Dendritic Pattern](https://github.com/mightyiam/dendritic)
- [flake-parts](https://flake.parts)
- [import-tree](https://github.com/denful/import-tree)
- [flake-parts-modules](https://flake.parts/options/flake-parts-modules.html)
- [vic/dendrix](https://vic.github.io/dendrix/Dendritic.html) - Extended documentation
