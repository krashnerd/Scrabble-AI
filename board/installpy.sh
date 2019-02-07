sudo apt-get update
sudo apt-get install -y --no-install-recommends \
        build-essential \
        libfreetype6-dev \
        libpng12-dev \
        libzmq3-dev \
        pkg-config \
        python3-dev \
        python3-numpy \
        python3-pip \
        python3-scipy \
        python3-matplotlib \
        python3-pandas \
        python3-tk \
        unzip
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*
