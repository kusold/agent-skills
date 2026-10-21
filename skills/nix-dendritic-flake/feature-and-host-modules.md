# Feature and Host Modules

How features span configuration classes, how hosts assemble them, the `flake.modules` storage pattern, and how shared top-level options replace `specialArgs`. These correspond to Steps 5-6 of the conversion in [SKILL.md](SKILL.md).

## Feature Modules

Feature modules set options across multiple configuration classes.

**admin.nix** - Cross-platform admin privileges:
```nix
{ config, ... }:
{
  flake.modules = {
    # NixOS: add user to wheel
    nixos.admin = {
      users.groups.wheel.members = [ config.username ];
    };

    # Darwin: set primary user
    darwin.admin = {
      system.primaryUser = config.username;
    };
  };
}
```

**shell.nix** - Cross-platform shell configuration:
```nix
{ config, lib, ... }:
{
  flake.modules = {
    nixos.shell = nixosArgs: {
      programs.fish.enable = true;
      users.users.${config.username}.shell = nixosArgs.config.programs.fish.package;
    };

    homeManager.shell = {
      programs.fish.enable = true;
      programs.starship.enable = true;
    };
  };
}
```

## Host Configuration Modules

**myhost.nix** - Specific host definition:
```nix
{ config, ... }:
let
  inherit (config.flake.modules) nixos homeManager;
in
{
  configurations.nixos.myhost.module = {
    imports = [
      nixos.admin
      nixos.shell
      # Hardware-specific imports
    ];

    nixpkgs.hostPlatform = "x86_64-linux";
    system.stateVersion = config.stateVersion;

    # Host-specific config
    networking.hostName = "myhost";
  };
}
```

## The flake.modules Pattern

`flakeModules.modules` from flake-parts provides the `flake.modules` option for storing lower-level modules grouped by module class (`nixos`, `darwin`, `homeManager`). It is a convenience - when the structure of your lower-level modules is itself part of your system model, prefer declaring your own options instead (see the Anti-patterns section in [SKILL.md](SKILL.md)):

```nix
# In any module file
{ config, ... }:
{
  flake.modules = {
    nixos.featureName = { ... }: {
      # NixOS module content
    };

    homeManager.featureName = { ... }: {
      # home-manager module content
    };

    darwin.featureName = { ... }: {
      # nix-darwin module content
    };
  };
}
```

**Usage in host configs:**
```nix
{ config, ... }:
let
  inherit (config.flake.modules) nixos homeManager;
in
{
  configurations.nixos.myhost.module = {
    imports = [ nixos.featureName nixos.otherFeature ];
  };
}
```

## deferredModule Semantics

`deferredModule` stores modules unevaluated - the target module system (NixOS, home-manager, nix-darwin) pays the evaluation cost when it imports the value. Semantics worth knowing when debugging:

- **Options inside a deferred module are invisible to the outer flake-parts system.** Outer modules cannot read them, `debug.options` will not list them, and type errors surface only when the host system evaluates - debug deferred module content at the host level, not in the flake-parts repl.
- **Multiple definitions of the same deferredModule option merge by concatenating `imports`** - that is why several feature modules can each contribute to one `configurations.nixos.<host>.module` (or any shared option) and compose cleanly.
- **`lib.types.deferredModuleWith { staticModules = ...; }`** is the escape hatch when the outer system needs visibility - the static modules' options become visible in the outer system's documentation.
- **`flake.modules` is class-typed.** Values are wrapped with `_class`, so loading a module under the wrong class (e.g. a `homeManager` module into `nixosSystem`) fails as a type error in class-aware evaluators rather than silently misconfiguring.

## import-tree Details

The `import-tree` flake auto-imports all `.nix` files recursively:

```nix
outputs = inputs:
  inputs.flake-parts.lib.mkFlake { inherit inputs; }
    (inputs.import-tree ./modules);
```

**Behavior:**
- Imports all `*.nix` files under `./modules` recursively
- Paths containing `/_` are ignored by default
- Each file becomes a flake-parts module

**Ignoring files:**
```
modules/
  _templates/     # Ignored (starts with _)
  _wip.nix        # Ignored
  feature.nix     # Imported
```

## Sharing Values Without specialArgs

**Anti-pattern (traditional):**
```nix
# Passing values via specialArgs
lib.nixosSystem {
  specialArgs = { inherit username scripts; };
  modules = [ ./configuration.nix ];
}
```

**Dendritic approach:**
```nix
# meta.nix - declare top-level option
{ lib, ... }:
{
  options.username = lib.mkOption {
    type = lib.types.str;
    default = "myuser";
  };
}

# feature.nix - read from top-level config
{ config, ... }:
{
  flake.modules.nixos.myFeature = {
    users.users.${config.username}.extraGroups = [ "docker" ];
  };
}
```

## Complete Example Structure

```
flake.nix
flake.lock
modules/
  # Infrastructure
  systems.nix
  flake-parts.nix
  meta.nix
  nixos.nix
  darwin.nix
  home-manager.nix

  # Features (cross-platform)
  shell.nix
  admin.nix
  git.nix
  editor.nix

  # Hosts
  desktop.nix
  laptop.nix
  server.nix

  # Platform-specific features
  linux/
    gaming.nix
    docker.nix
  darwin/
    homebrew.nix
```
