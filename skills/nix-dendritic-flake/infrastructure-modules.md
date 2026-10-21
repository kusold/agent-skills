# Infrastructure Modules

Full source for the core infrastructure of a dendritic flake: target systems, flake-parts extras, shared top-level options, and the per-class configuration plumbing for NixOS, home-manager, and nix-darwin. These correspond to Steps 3-4 of the conversion in [SKILL.md](SKILL.md).

## systems.nix - Define Target Systems

```nix
{
  systems = [
    "x86_64-linux"
    "aarch64-linux"
    "aarch64-darwin"
  ];
}
```

## flake-parts.nix - Import flake-parts Extras

```nix
{ inputs, ... }:
{
  imports = [
    # Provides flake.modules option for deferredModules
    inputs.flake-parts.flakeModules.modules
  ];
}
```

## meta.nix - Declare Shared Top-Level Options

Move values you used to pass via `specialArgs` into top-level options. Keep them settable - `readOnly = true` would freeze each value in this file instead of letting hosts or users override it:

```nix
{ lib, ... }:
{
  options.username = lib.mkOption {
    type = lib.types.singleLineStr;
    default = "myuser";
  };

  options.stateVersion = lib.mkOption {
    type = lib.types.str;
    default = "24.11";
  };
}
```

## nixos.nix - NixOS Configuration Infrastructure

Turns `configurations.nixos.<name>.module` into `flake.nixosConfigurations` and generates `flake.checks` for each configuration's toplevel:

```nix
{ lib, config, ... }:
{
  options.configurations.nixos = lib.mkOption {
    type = lib.types.lazyAttrsOf (
      lib.types.submodule {
        options.module = lib.mkOption {
          type = lib.types.deferredModule;
        };
      }
    );
    default = {};
  };

  config.flake = {
    nixosConfigurations = lib.mapAttrs (
      name: { module }: lib.nixosSystem { modules = [ module ]; }
    ) config.configurations.nixos;

    # Add checks for each configuration's toplevel
    checks = lib.mkMerge (
      lib.mapAttrsToList (
        name: nixos: {
          ${nixos.config.nixpkgs.hostPlatform.system} = {
            "configurations:nixos:${name}" = nixos.config.system.build.toplevel;
          };
        }
      ) config.flake.nixosConfigurations
    );
  };
}
```

## home-manager.nix - home-manager Configuration Infrastructure

```nix
{ lib, config, inputs, ... }:
{
  options.configurations.homeManager = lib.mkOption {
    type = lib.types.lazyAttrsOf (
      lib.types.submodule {
        options.module = lib.mkOption {
          type = lib.types.deferredModule;
        };
      }
    );
    default = {};
  };

  config.flake.homeConfigurations = lib.mapAttrs (
    name: { module }:
      inputs.home-manager.lib.homeManagerConfiguration {
        pkgs = inputs.nixpkgs.legacyPackages.x86_64-linux;
        modules = [ module ];
      }
  ) config.configurations.homeManager;
}
```

> **Note:** `pkgs` is hardcoded to `x86_64-linux` here for brevity. Derive it per configuration and system (e.g. store `system` alongside `module` in the submodule and `import inputs.nixpkgs { system = ...; }`) so aarch64-linux and Darwin hosts work.

## darwin.nix - nix-darwin Configuration Infrastructure

```nix
{ lib, config, inputs, ... }:
{
  options.configurations.darwin = lib.mkOption {
    type = lib.types.lazyAttrsOf (
      lib.types.submodule {
        options.module = lib.mkOption {
          type = lib.types.deferredModule;
        };
      }
    );
    default = {};
  };

  config.flake.darwinConfigurations = lib.mapAttrs (
    name: { module }:
      inputs.nix-darwin.lib.darwinSystem {
        modules = [ module ];
      }
  ) config.configurations.darwin;
}
```

All three infrastructure modules share the same shape: a `configurations.<class>` option of `lazyAttrsOf (submodule { module = deferredModule; })`, mapped into the matching flake output. Add a new class (e.g. `nixos-darwin` combined configs) by following the same template.

Since each host's toplevel lands in `flake.checks`, a plain `nix flake check` builds every host closure - use `nix flake check --no-build` for eval-only iteration (see Best Practices in [SKILL.md](SKILL.md)).
