# SLAM Thesis

See [thesis.pdf](output/thesis.pdf) for the latest version of this thesis.

## Dependencies

Instructions tested on Ubuntu 20.04.

- Download texlive 2021.
  ```bash
  sudo apt-get remove texlive*
  sudo rm -rf /usr/local/texlive
  sudo mkdir -p /usr/local/texlive
  sudo chown -R $USER /usr/local/texlive

  wget ftp://tug.org/historic/systems/texlive/2021/install-tl-unx.tar.gz
  tar -xvf install-tl-unx.tar.gz
  ./install-tl -repository ftp://tug.org/historic/systems/texlive/2021/tlnet-final
  # Then enter option `i` in interactive prompt (will likely take hours to install)
  # And finally add this to your .bashrc or equivalent
  # export PATH=/usr/local/texlive/2021/bin/x86_64-linux:$PATH
  ```

- Install [gpp 2.27](https://github.com/logological/gpp/releases/tag/2.27)
  ```bash
  wget https://github.com/logological/gpp/releases/download/2.27/gpp-2.27.tar.bz2
  tar -xvf gpp-2.27.tar.bz2
  cd gpp-2.27-tar.bz2
  ./configure
  make
  # Add the binary in src/gpp to your PATH
  ```

- Get [pandoc 2.16.2](https://github.com/jgm/pandoc/releases/tag/2.16.2)
  ```bash
  wget https://github.com/jgm/pandoc/releases/download/2.16.2/pandoc-2.16.2-1-amd64.deb
  sudo dpkg -i pandoc-2.16.2-1-amd64.deb
  ```

- Install `pip install pandocfilters=1.4.3` (python 3.8.10)

- Run `./install_linux.sh`

## Build

Run `make pdf`

There is also make targets: `md`, `tex` and `pdfast` (pdf without bibtex)
