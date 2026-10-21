---
name: nix-module-options
description: Query NixOS and Home Manager module options programmatically using flake evaluation. Works in any flake with a nixpkgs input; flake-parts flakes with debug = true additionally reuse your overlay-aware pkgs. Use this skill when the user asks to check if a module exists, explore available options, get option documentation, or verify what options are available in upstream NixOS/Home Manager (not custom user modules). Activates for queries like "does home manager have a module for X", "what options does service Y have", "check nixos options for Z", or "explore available options".
metadata:
  source: https://github.com/Omegaice/dotfiles/blob/master/.claude/skills/nix-module-options/SKILL.md
  version: "1.1.0"
---

# Nix Module Options Explorer

Expert guidance for programmatically querying NixOS and Home Manager module options using flake evaluation.

## Core Capability

Ready-made `nix eval --impure` expressions that evaluate the upstream NixOS and Home Manager option trees from your flake's locked inputs: option existence, full documentation, and category listings as JSON.

## Prerequisites

- **nix** (with flakes) and **jq**
- Run from inside a flake repository — expressions use `builtins.getFlake (builtins.toString ./.)`
- A `nixpkgs` flake input (any flake); a `home-manager` input additionally for Home Manager queries
- Optional: a flake-parts flake with `debug = true;` set in one of its modules (Backend A — overlay-aware `pkgs`; measured at the same speed as Backend B)

## Selecting a Backend

Detect which backend your flake supports:

```bash
nix eval --impure --expr '(builtins.getFlake (builtins.toString ./.)) ? currentSystem'
```

- `true` → **Backend A (flake-parts)** — reuses your pre-evaluated, overlay-aware `pkgs` via `currentSystem.allModuleArgs`. Requires `debug = true;` in a flake-parts module. Speed is at parity with Backend B — choose it for overlay-awareness.
- `false` → **Backend B (any flake)** — instantiates `pkgs` from `flake.inputs.nixpkgs` directly. Works in any flake with a `nixpkgs` input; not overlay-aware.

Both backends expose identical names to queries: `lib`, `hmLib`, `hmOpts` (Home Manager option tree), `nixosOpts` (NixOS option tree). Nix is lazy — only the option tree your query touches gets evaluated.

## Backend A: flake-parts (`debug = true`)

```bash
nix eval --impure --expr '
  let
    flake = builtins.getFlake (builtins.toString ./.);
    args = flake.currentSystem.allModuleArgs;
    lib = args.pkgs.lib;
    hmLib = lib.extend (self: super: {
      hm = import "${flake.inputs.home-manager}/modules/lib" { lib = self; };
    });
    hmOpts = (hmLib.evalModules {
      modules = import "${flake.inputs.home-manager}/modules/modules.nix" {
        lib = hmLib;
        pkgs = args.pkgs;
        check = false;
      };
    }).options;
    nixosOpts = (lib.evalModules {
      modules = import "${flake.inputs.nixpkgs}/nixos/modules/module-list.nix" ++ [
        { nixpkgs.hostPlatform = args.system; }
      ];
    }).options;
  in
    QUERY
'
```

## Backend B: any flake (nixpkgs input only)

```bash
nix eval --impure --expr '
  let
    flake = builtins.getFlake (builtins.toString ./.);
    system = builtins.currentSystem;
    pkgs = import flake.inputs.nixpkgs { inherit system; };
    lib = pkgs.lib;
    hmLib = lib.extend (self: super: {
      hm = import "${flake.inputs.home-manager}/modules/lib" { lib = self; };
    });
    hmOpts = (hmLib.evalModules {
      modules = import "${flake.inputs.home-manager}/modules/modules.nix" {
        lib = hmLib;
        inherit pkgs;
        check = false;
      };
    }).options;
    nixosOpts = (lib.evalModules {
      modules = import "${flake.inputs.nixpkgs}/nixos/modules/module-list.nix" ++ [
        { nixpkgs.hostPlatform = system; }
      ];
    }).options;
  in
    QUERY
'
```

## Query Catalog

Substitute any entry for `QUERY` in the backend expression above. The `hmOpts`/`nixosOpts` patterns are interchangeable.

### Check if an option exists

Add `--apply 'o: o != null'` to the `nix eval` command — it prints `true` or `false` directly (no jq needed):

- Home Manager: `hmOpts.programs.duf.enable or null`
- NixOS: `nixosOpts.services.nginx.enable or null`

`--apply 'o: o != null'` compares the result against null without forcing the option's contents, so it works on every nixpkgs version (no reliance on value serialization).

### Get full option documentation

Pipe to `jq` for readable output:

- `lib.optionAttrSetToDocList hmOpts.programs.git`
- `lib.optionAttrSetToDocList nixosOpts.services.nginx.virtualHosts`

### List all options in a category

Add `| jq -r '.[]'`:

- `builtins.attrNames hmOpts.programs`
- `builtins.attrNames nixosOpts.services`

### Option paths with literal dots

Quote the segment: `nixosOpts.services.nginx.virtualHosts."foo.bar"`. Unquoted, `foo.bar` parses as nested attributes `foo` → `bar`.

## Session Mode: Batch Queries in One `nix repl`

Every `nix eval` invocation re-pays the module-tree merge (~1s for Home Manager, ~2.5–3.7s for NixOS warm) — the merge dominates, so query shape barely matters. For **2–3 or more queries in one task** (the common "does it exist → what options → what defaults" flow), load the backend once in a single `nix repl` session and issue every query there: measured ~3× faster for 5 queries (2.7s vs 7.4s as separate spawns), ~30ms per additional query after load. `nix repl` is impure by default, even on machines with `pure-eval = true`.

Pipe the backend's bindings as repl **assignments** — a top-level `let … in` does NOT define repl bindings and silently discards them:

```bash
nix repl <<'EOF'
# Backend B bindings (works in any flake)
f = builtins.getFlake (builtins.toString ./.)
pkgs = import f.inputs.nixpkgs { system = builtins.currentSystem; }
lib = pkgs.lib
hmLib = lib.extend (self: super: {
  hm = import "${f.inputs.home-manager}/modules/lib" { lib = self; };
})
hmOpts = (hmLib.evalModules {
  modules = import "${f.inputs.home-manager}/modules/modules.nix" {
    lib = hmLib; inherit pkgs; check = false;
  };
}).options
nixosOpts = (lib.evalModules {
  modules = import "${f.inputs.nixpkgs}/nixos/modules/module-list.nix" ++ [
    { nixpkgs.hostPlatform = builtins.currentSystem; }
  ];
}).options

# Queries — any entry from the Query Catalog, one per line
nixosOpts.services.nginx.enable or null
lib.optionAttrSetToDocList hmOpts.programs.git
builtins.attrNames hmOpts.programs
:q
EOF
```

For Backend A, replace the first two binding lines with `args = f.currentSystem.allModuleArgs;` and `pkgs = args.pkgs;`, and use `nixpkgs.hostPlatform = args.system;`.

## Common Option Categories

**Home Manager top-level:**
- `programs.*` - User programs (git, vim, zsh, etc.)
- `services.*` - User services (gpg-agent, syncthing, etc.)
- `home.*` - Home directory settings
- `xdg.*` - XDG directory configuration
- `accounts.*` - Email, calendar accounts
- `systemd.*` - User systemd units
- `gtk.*`, `qt.*` - Desktop theming
- `wayland.*` - Wayland compositors

**NixOS top-level:**
- `services.*` - System services (nginx, postgresql, etc.)
- `programs.*` - System-wide programs
- `hardware.*` - Hardware configuration
- `boot.*` - Boot loader and kernel
- `networking.*` - Network configuration
- `environment.*` - System environment
- `systemd.*` - System units
- `users.*` - User management
- `virtualisation.*` - Containers, VMs
- `security.*` - Security settings

## Option Documentation Fields

`lib.optionAttrSetToDocList` returns structured documentation:

- **name** - Full option path (e.g., `programs.git.enable`)
- **description** - What the option does (markdown formatted)
- **type** - Expected value type (e.g., `boolean`, `string`, `list of string`)
- **default** - Default value if not set
- **example** - Usage examples
- **declarations** - Source file where option is defined
- **visible** - Whether option appears in documentation
- **readOnly** - Whether option can be modified
- **internal** - Whether option is internal-only

## Usage Patterns

- "Does home manager have a duf module?" → existence check on `hmOpts.programs.duf.enable`
- "What options does `programs.git` have?" → `lib.optionAttrSetToDocList hmOpts.programs.git` piped to `jq 'map(select(.visible == true)) | map({name, type, description})'`
- "What programs are available in home manager?" → category listing: `builtins.attrNames hmOpts.programs`
- "Get the default for `services.nginx.enable`" → full docs, read the `default` field

## Technical Details

### Why `currentSystem.allModuleArgs` (Backend A)?

1. **Pre-evaluated** - `pkgs` already instantiated by flake-parts
2. **System-aware** - `args.system` provides the current system automatically
3. **Overlay-aware** - uses your instantiated `pkgs`, so your overlays can surface in the rendered defaults of `package`-type options
4. **Same speed as Backend B** - measured at parity; the module-tree merge dominates both backends. Choose Backend A for the overlay-aware `pkgs`, not for speed.

Backend B re-instantiates `pkgs` without your overlays, so package-option defaults reflect plain nixpkgs.

### Purity Guarantees

These expressions query **upstream modules only**:
- Imports directly from `${flake.inputs.home-manager}/modules/modules.nix`
- Imports directly from `${flake.inputs.nixpkgs}/nixos/modules/module-list.nix`
- Does NOT include user's custom modules from `.claude/` or `home/`
- Does NOT evaluate user's actual `homeConfigurations` or `nixosConfigurations`

To query user's actual config (including custom modules):
```bash
nix eval --impure --expr '
  (builtins.getFlake (builtins.toString ./.))
  .homeConfigurations.USERNAME.options.OPTION.PATH
'
```

## Best Practices

1. **Use `jq` for filtering** - Pipe documentation output to `jq` for readable results
2. **Filter visible options** - Use `select(.visible == true)` to hide internal options
3. **Check existence first** - `--apply 'o: o != null'` before pulling full docs
4. **Reference declarations** - Use `.declarations` field to find upstream source
5. **Batch with Session Mode** - For 2–3+ queries, one `nix repl` session beats repeated `nix eval` spawns ~3×
6. **Approximate lookups** - When the pinned revision doesn't matter, instant channel-snapshot sources exist (home-manager-options.extranix.com static JSON, search.nixos.org options API) — but they are channel snapshots, not your lockfile

## Troubleshooting

### `error: attribute 'currentSystem' missing`
The `currentSystem` (and `allSystems`, `debug`) flake outputs exist only when a flake-parts module sets `debug = true;`. Either:
- Enable it: add `debug = true;` to one of your flake-parts modules and **commit (or at least `git add`) the change** — `builtins.getFlake` reads the git tree, so uncommitted edits are invisible. Then use Backend A.
- Or skip it: use Backend B, which needs no flake-parts at all.

### "path does not exist" error
The flake path must exist. This skill uses `builtins.getFlake (builtins.toString ./.)` which refers to the current project directory. Ensure you're running commands from within your flake repository.

### "attribute does not exist" error
The option path is wrong. Check:
- Correct category (e.g., `programs` vs `services`)
- Correct nesting (e.g., `programs.git.enable` not `programs.git`)
- Option exists in upstream (not a custom module)
- Segments containing literal dots must be quoted: `nixosOpts.services.nginx.virtualHosts."foo.bar"`
- Category paths like `nixosOpts.services` are attribute sets, not options — they trivially "exist"; existence checks are only meaningful for leaf options

### Evaluation timing
Each query re-pays the upstream option-tree merge: ~1s for Home Manager, ~2.5–3.7s for NixOS warm on a fast machine, much longer cold while locked inputs are fetched. Query shape barely matters — existence checks, full docs, and category listings cost about the same, because the merge dominates. Separate `nix eval` spawns re-pay that merge every time: Nix's eval cache never serves values to `nix eval` (only leaf attrpath metadata is cached; intermediate results are not). Use Session Mode for multiple queries. For heavy recurring use, materialize the docs once as a derivation (`lib.nixosOptionsDoc`, Home Manager's `lib.hmOptionsDoc`) and `nix build` it — the build cache does persist built results, unlike the eval cache.

### Wrong module system
- Home Manager queries use `hmOpts` (HM modules via `hmLib.evalModules`)
- NixOS queries use `nixosOpts` (NixOS modules via `lib.evalModules`)

## Related Skills

- **[nix-flake-parts](../nix-flake-parts/SKILL.md)** - the flake-parts framework skill; its Debugging section documents the `debug = true;` output and `currentSystem.allModuleArgs` infrastructure Backend A builds on
- **[nix-dendritic-flake](../nix-dendritic-flake/SKILL.md)** - every-file-is-a-top-level-module flake architecture built on flake-parts
