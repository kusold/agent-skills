---
name: nix-flake-parts
description: Expert guidance for the flake-parts framework in Nix flakes. Use when converting flakes to flake-parts ("convert my flake to flake-parts"), organizing modular flake configurations, working with perSystem ("how do perSystem and flake differ?"), creating reusable flake modules, handling overlays, or debugging flake-parts issues ("why is `final` undefined", "argument 'pkgs' missing"). For the architecture where every file is a top-level module, use nix-dendritic-flake.
metadata:
  credits:
    skill: using-flake-parts
    author: Omegaice
    url: "https://github.com/Omegaice/dotfiles/blob/master/.claude/skills/using-flake-parts/SKILL.md"
---

# Flake-Parts Expert

Specialized guidance for the flake-parts framework — a modular system for organizing Nix flakes. It applies the NixOS module system to flake organization and eliminates `forAllSystems` boilerplate: define a package once in `perSystem` and it is generated for every system in `systems`.

## Structure with mkFlake

```nix
{
  inputs.flake-parts.url = "github:hercules-ci/flake-parts";

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      # Target architectures - define once
      systems = [ "x86_64-linux" "aarch64-linux" ];

      # External modules
      imports = [ ./modules/packages.nix ];

      # Multi-system configuration (defined once, generated for all systems)
      perSystem = { config, pkgs, ... }: {
        packages.hello = pkgs.hello;
        devShells.default = pkgs.mkShell {
          packages = [ config.packages.hello ];
        };
      };

      # Traditional flake-level attributes (single-system)
      flake = {
        nixosConfigurations.machine = { };
      };
    };
}
```

**Generated structure:**

```nix
# Input:
perSystem.packages.hello = pkgs.hello;

# Output:
packages.x86_64-linux.hello = <derivation>;
packages.aarch64-linux.hello = <derivation>;
```

## perSystem vs flake

**Use `perSystem` for things that build across multiple platforms:**
- Packages, devShells, apps
- Formatters, checks
- Anything that should exist per-system

**Use `flake` for unique, non-system-specific outputs:**
- `nixosConfigurations` (each machine is unique)
- `homeConfigurations` (each config is unique)
- Custom flake outputs

### Standard perSystem Options

- **`packages`** - Derivations to build (e.g., `packages.myapp = pkgs.hello;`)
- **`apps`** - Executable applications (for `nix run`)
- **`devShells`** - Development environments (for `nix develop`)
- **`checks`** - Tests and validation (run with `nix flake check`)
- **`formatter`** - Code formatter (single package, run with `nix fmt`)
- **`legacyPackages`** - Nested, unvalidated package sets; traversed cheaply (name-level) by `nix flake check`, skipped by `nix flake show` unless `--legacy`

All are automatically generated for each system in the `systems` list.

## Module Arguments

Only arguments you **name in the function signature** are passed — the module system inspects signatures with `builtins.functionArgs`. A catch-all `args:` receives none of the special arguments.

| Argument | Scope | Purpose |
|----------|-------|---------|
| `pkgs` | perSystem | nixpkgs for the current system |
| `system` | perSystem | Current architecture string |
| `config` | both | Access other values in the current configuration |
| `inputs'` | perSystem | Inputs with system auto-selected (`inputs'.foo.packages.bar`) |
| `self'` | perSystem | This flake's outputs with system pre-selected |
| `final` | perSystem (with easyOverlay) | Package set after overlays — see [overlays.md](overlays.md) |
| `inputs` | top level only | The flake's inputs attrset |
| `withSystem` | top level only | Enter a system's scope (see below) |
| `getSystem` | top level only | Retrieve a specific system's perSystem config |
| `moduleWithSystem` | top level only | Export modules with access to this flake’s perSystem arguments |

`inputs`, `self`, `withSystem`, `getSystem`, and `moduleWithSystem` are top-level arguments only — current flake-parts throws if you name them in a `perSystem` signature. Inside `perSystem`, use `inputs'` and `self'`.

```nix
perSystem = { pkgs, system, inputs', self', ... }: {
  packages.myapp = pkgs.writeShellScriptBin "myapp" "echo hello on ${system}";
  packages.tool = inputs'.some-flake.packages.default;
  devShells.default = pkgs.mkShell {
    packages = [ self'.packages.myapp ];
  };
};
```

**The @ pattern** captures the arguments of the function where it appears. Bind it on the outer module to retain top-level `config` when `perSystem` names its own `config`:

```nix
toplevel@{ config, ... }: {
  systems = [ "x86_64-linux" ];

  perSystem = { config, pkgs, ... }: {
    # config          = per-system config
    # toplevel.config = top-level config
    packages.example = pkgs.writeText "target-systems"
      (builtins.concatStringsSep "," toplevel.config.systems);
  };
}
```

Full reference — `_module.args` customization, `functionArgs` inspection, pitfalls — in [module-arguments.md](module-arguments.md).

### withSystem: bridging to single-system outputs

`withSystem` enters a system's scope so `flake`-level outputs (like NixOS configs) can use perSystem values. Bind `inputs` at the top level; the callback only receives perSystem arguments:

```nix
{ inputs, withSystem, ... }: {
  flake.nixosConfigurations.machine = withSystem "x86_64-linux" (
    { config, ... }:
      inputs.nixpkgs.lib.nixosSystem {
        modules = [{
          environment.systemPackages = [ config.packages.myapp ];
        }];
      }
  );
}
```

Without `withSystem`: `self.packages.x86_64-linux.myapp` (repetitive and verbose).

## Converting a Standard Flake

**Before converting**: confirm the flake is under version control with a clean tree (commit or stash first). Migrate one output at a time and validate with `nix flake check --no-build` between steps — evaluation-only, so you get the same module-system validation without building every `checks` derivation at each step. New files must be git-tracked before the flake can see them (`git add -N file.nix`). For final validation run a full `nix flake check --all-systems` (by default `flake check` omits non-current systems), or [nix-fast-build](https://github.com/Mic92/nix-fast-build) in CI for parallel eval+build.

**Before:**

```nix
outputs = { nixpkgs, ... }:
  let
    systems = [ "x86_64-linux" "aarch64-linux" ];
    forAllSystems = nixpkgs.lib.genAttrs systems;
  in {
    packages = forAllSystems (system: {
      hello = nixpkgs.legacyPackages.${system}.hello;
    });
  };
```

**After:**

```nix
outputs = inputs@{ flake-parts, ... }:
  flake-parts.lib.mkFlake { inherit inputs; } {
    systems = [ "x86_64-linux" "aarch64-linux" ];
    perSystem = { pkgs, ... }: {
      packages.hello = pkgs.hello;
    };
  };
```

**Why `perSystem` over `eachSystem` helpers**: flake-parts transposes per-system outputs lazily — requesting `packages.x86_64-linux.foo` evaluates only that system. flake-utils' `eachSystem` eagerly fold-merges every system's outputs, which measured 3.2× slower on a full `nix flake check` at 8 systems (point evals are equal), and every consumer adds its own `flake-utils` entry to the lock file. Prefer `perSystem` or plain `lib.genAttrs`.

Step-by-step migration, incremental old/new mixing, and a checklist: [advanced.md](advanced.md).

## Beyond the Basics

- **[module-arguments.md](module-arguments.md)** - Complete reference for all module arguments, the @ pattern, `functionArgs` inspection, and `_module.args` customization
- **[overlays.md](overlays.md)** - easyOverlay: auto-generate overlays from perSystem packages, the `final` vs `pkgs` distinction, pitfalls. Import it at the **top level** (`imports = [ inputs.flake-parts.flakeModules.easyOverlay ];`), never inside `perSystem`
- **[modular-organization.md](modular-organization.md)** - `importApply` for passing flake-level context (like `withSystem`) into imported modules; reusable `flakeModules`; dogfooding your own modules
- **[advanced.md](advanced.md)** - Partitions (isolated evaluation via `partitionedAttrs`), custom outputs, debug mode, migration from standard flakes

## Best Practices

1. **Don't traverse inputs** - Never iterate through `inputs` with `mapAttrs` or similar (causes unnecessary fetching and evaluation)
2. **Namespace options** - Use `mymodule.foo` not just `foo` to avoid collisions
3. **Favor perSystem** - Most work happens there (packages, shells, checks)
4. **Use specific options** - Prefer `foo.package` over `foo.flake` for better granularity
5. **Use `'` suffixed arguments** - Prefer `inputs'` and `self'` over manual system selection

## Debugging

Enable debug mode:

```nix
{
  debug = true;
  # ... rest of config
}
```

Inspect with `nix repl`:

```bash
nix repl
:lf .
currentSystem.allModuleArgs.pkgs        # Inspect current system pkgs
debug.allSystems.x86_64-linux           # Inspect specific system
currentSystem.options.packages.files    # See where values are defined
debug.options.systems.declarations      # See where options are declared
```

Debug mode adds no measurable evaluation overhead, but it *publishes* `debug`, `allSystems`, and `currentSystem` (impure contexts only) as public flake outputs — turn it off when you're done for output hygiene, not speed.

The **nix-module-options** skill builds on this `debug = true` infrastructure to query upstream NixOS/Home Manager options via `currentSystem.allModuleArgs`.

## Common Issues

### "path does not exist" Error

Files must be git-tracked for flakes to see them:

```bash
git add <your-module-files>
# OR for quick testing:
git add -N file.nix  # Track without staging content
```

### Circular Dependency

Don't access `self` directly in modules. In `perSystem`, use `self'` or `config`; from flake level, use `withSystem`.

### Wrong Module Context

Use `@` syntax to access both top-level and perSystem config:

```nix
toplevel@{ config, ... }: {
  perSystem = { config, ... }: {
    # config = perSystem config
    # toplevel.config = top-level config
  };
}
```

### Undefined Variable in Module Argument

The module system only passes arguments you explicitly name:

```nix
# ✅ CORRECT
{ pkgs, system, config, ... }: { }

# ❌ WRONG
args: { }  # Won't receive special arguments
```

## Related Skills

- **nix-dendritic-flake** - Convert flakes to the dendritic pattern (every file is a top-level flake-parts module)
- **nix-module-options** - Query upstream NixOS/Home Manager module options programmatically (uses this skill's `debug = true` outputs)
