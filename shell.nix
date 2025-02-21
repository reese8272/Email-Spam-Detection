{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = with pkgs; [
    poetry
    python3
    python3Packages.numpy
    python3Packages.gradio
    ollama
    gcc
    libgcc
    gnumake
    cmake
    extra-cmake-modules
  ];

    shellHook = ''
        ollama serve > output/ollama_output.txt &
    '';
}
