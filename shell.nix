let
  pkgs = import <nixpkgs> {};
  python = pkgs.python311;
  pythonPackages = python.pkgs;

in with pkgs; mkShell {

  buildInputs = with pkgs; [
    python311
    python311Packages.numpy
    python311Packages.gradio
    python311Packages.tensorflow
    python311Packages.pandas
    python311Packages.keras
    python311Packages.requests
    python311Packages.pytest
  ];

  shellHook = ''
    export PATH="${pkgs.python311}/bin:$PATH"
    VENV=.venv
    export TF_CFLAGS="-march=native -mavx -msse3 -msse4.1 -msse4.2 -mfma -mavx2"
    export TF_CPP_MIN_LOG_LEVEL=2


    if [ ! -d "$VENV" ]; then
      python -m venv $VENV
    fi


    source ./$VENV/bin/activate
    export PYTHONPATH=`pwd`/$VENV/${python.sitePackages}/:$PYTHONPATH


    # if [ ! -f "$VENV/lib/python${python.version}/site-packages/numpy" ]; then
    #   pip install -r requirements.txt
    # fi
  '';
}
