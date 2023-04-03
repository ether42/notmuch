# https://stackoverflow.com/questions/63966084/what-is-the-equivalent-shell-nix-for-nix-shell-nixpkgs-a-gnused
let
  pkgs = import <nixpkgs> {
    overlays = [
      (self: super: {
        xapian = super.xapian.overrideAttrs (old: {
          NIX_CFLAGS_COMPILE = "-fsanitize=thread -g3 -O0";
          doCheck = false;
        });
        sfsexp = super.enableDebugging (super.sfsexp.overrideAttrs (old: rec {
          doCheck = false;
          version = "1.4.1";
          src = super.fetchFromGitHub {
            owner = "mjsottile";
            repo = "sfsexp";
            rev = "v${version}";
            sha256 = "sha256-uAk/8Emf23J0D3D5+eUEpWLY2fIvdQ7a80eGe9i1WQ8=";
          };
        }));
      })
    ];
  };
in
pkgs.mkShell {
  nativeBuildInputs = with pkgs; [
    pkg-config

    # nativeCheckInputs
    bash
    dtach
    # emacs
    gdb
    man
    openssl
    which
  ];
  buildInputs = with pkgs; [
    gmime3
    gnupg
    perl
    python3
    sfsexp
    talloc
    xapian
    zlib
  ];
}
