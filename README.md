# kivy-tasks-client

### Install commands for kivy on Ubuntu:

```bash
# add kivy repository
sudo add-apt-repository ppa:kivy-team/kivy
sudo apt-get update

# install kivy for python3 and kivy examples
sudo apt-get install python3-kivy python-kivy-examples

# install some required dependencies for pygame and cython
sudo apt-get install -y \
    python3-pip \
    build-essential \
    mercurial \
    git \
    python3 \
    python3-dev \
    ffmpeg \
    libsdl-image1.2-dev \
    libsdl-mixer1.2-dev \
    libsdl-ttf2.0-dev \
    libsmpeg-dev \
    libsdl1.2-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev

# install some more dependencies
pip3 install numpy
pip3 install Cython==0.21.2
pip3 install hg+http://bitbucket.org/pygame/pygame
pip3 install git+https://github.com/kivy/buildozer.git@master
pip3 install git+https://github.com/kivy/plyer.git@master
pip3 install -U pygments docutils
pip3 install requests

# and finally, install kivy
pip3 install kivy
```

### Install Kivy Garden and widgets:

From the above install sequence the garden tool script will be installed in ```~/.local/bin/garden```

##### Modify the script according to [this article](http://advinpy.blogspot.ro/2015/12/kivy-garden-fixed-to-fertile-land-again.html).

```python
# add to the beginning of file
from io import BytesIO

# in the download(...) function modify the following:
# ...
data = ''
# to
data = b''  # initialize with an empty bytearray
# ...
# and
# ...
return StringIO(data)
# to
return BytesIO(data)
# ...
```

##### Install garden widgets by running the garden script. Example:

```bash
./garden install circularlayout
./garden install circulardatetimepicker
# note: for the circular datetime picker to work with python 3 you need to
# replace all occurences of xrange with range.
```