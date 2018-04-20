# av-stremer

Working with [PyAV](https://github.com/mikeboers/PyAV) and [FFmpeg](https://github.com/FFmpeg/FFmpeg)

Full documentation [PyAV Docs](http://mikeboers.github.io/PyAV/index.html) and [FFmpeg Docs](http://ffmpeg.org/documentation.html)

How install [PyAV Install](http://mikeboers.github.io/PyAV/installation.html)

Installation example

    sudo apt-get install ffmpeg x264
    
    sudo apt-get install -y python-dev pkg-config
    
    sudo apt-get install -y \
        libavformat-dev libavcodec-dev libavdevice-dev \
        libavutil-dev libswscale-dev libavresample-dev libavfilter-dev
    
    pip install av


sudo apt-get update
sudo apt-get -y install autoconf automake build-essential libass-dev libfreetype6-dev libtheora-dev libtool libvorbis-dev pkg-config texinfo zlib1g-dev 

sudo apt-get install x264 libx264-dev
sudo apt-get install libfdk-aac-dev
sudo apt-get install libmp3lame-dev
sudo apt-get install yasm

./configure —enable-network —enable-protocol=tcp —enable-demuxer=rtsp —enable-decoder=h264 —disable-static —enable-shared —disable-doc —enable-libass —enable-libfdk-aac —enable-libfreetype —enable-libtheora —enable-libvorbis —enable-libmp3lame —enable-nonfree —enable-gpl

./configure --enable-network --enable-protocol=tcp --enable-demuxer=rtsp --enable-decoder=h264 --disable-static --enable-shared --disable-doc --enable-libass --enable-libfdk-aac --enable-libfreetype --enable-libtheora --enable-libvorbis --enable-libmp3lame --enable-nonfree --enable-gpl --enable-libx26

make
sudo make install
sudo ldconfig

sudo apt-get install yasm libvpx-dev libx264-dev

./configure --enable-network --enable-protocol=tcp --enable-demuxer=rtsp --enable-decoder=h264 --disable-static --enable-shared --disable-doc --enable-libass --enable-libfdk-aac --enable-libfreetype --enable-libtheora --enable-libvpx --enable-libvorbis --enable-libmp3lame --enable-nonfree --enable-gpl --enable-libx264
