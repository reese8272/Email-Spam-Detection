{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    ollama
  ];

    shellHook = ''
        ollama serve > ollama_output.txt &
    '';
}
