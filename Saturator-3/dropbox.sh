cd ~ && wget -O - "https://www.dropbox.com/download?plat=lnx.x86_64" | tar xzf -
sudo apt-add-repository ppa:texlive-backports/ppa
sudo apt-get install -y texlive-lang-cjk
