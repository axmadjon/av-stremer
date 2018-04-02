import os

import av


class Stream:
    def __init__(self, **kwargs):
        if kwargs['output']:
            self.output = kwargs['output']

        elif kwargs['path'] and kwargs['filename']:
            path = kwargs['path']
            filename = kwargs['filename']

            if not os.path.exists(path):
                os.makedirs(path)

            self.output = av.open(os.path.join(path, filename), 'w')
        else:
            raise ValueError(str(kwargs))

        self.output_stream = None

    def add_stream(self, input_stream):
        pass

    def can_run(self, packet):
        return False

    def run(self, packet):
        pass

    def close(self):
        self.output.close()


class VideoOutput(Stream):
    def add_stream(self, input_stream):
        if input_stream is None:
            return

        self.output_stream = self.output.add_stream(codec_name='mpeg4', rate=input_stream.rate)
        self.output_stream.pix_fmt = input_stream.pix_fmt
        self.output_stream.width = input_stream.width
        self.output_stream.height = input_stream.height
        self.output_stream.options = {}

    def can_run(self, packet):
        return packet.stream.type == b'video'

    def run(self, packet):
        if not self.can_run(packet) or not self.output_stream:
            return

        try:
            for frame in packet.decode():
                cv2_image = frame.to_nd_array(format='bgr24')
                if hasattr(self, 'image_callback'):
                    getattr(self, 'image_callback')(cv2_image)

                frame = av.VideoFrame.from_ndarray(cv2_image, format='bgr24')
                for packet in self.output_stream.encode(frame):
                    self.output.mux(packet)
        except Exception as e:
            print ('Error on run VideoOutput {}'.format(e))


class AudioOutput(Stream):
    def add_stream(self, input_stream):
        self.output_stream = self.output.add_stream(codec_name='mp3')
        self.output_stream.options = {}

    def can_run(self, packet):
        return packet.stream.type == b'audio'

    def run(self, packet):
        if not self.can_run(packet) or not self.output_stream:
            return

        try:
            for frame in packet.decode():
                frame.pts = None
                for packet in self.output_stream.encode(frame):
                    self.output.mux(packet)

        except Exception as e:
            print('Error on run AudioOutput {}'.format(e))


class OutputStream:
    def __init__(self, path, filename):
        self.__output = av.open(os.path.join(path, filename), 'w')

        self.__video = VideoOutput(output=self.__output)
        self.__audio = AudioOutput(output=self.__output)

    def set_input(self, input):
        video_stream = input.get_stream('video')

        if video_stream:
            self.__video.add_stream(video_stream)

        audio_stream = input.get_stream('audio')
        if audio_stream:
            self.__audio.add_stream(audio_stream)

    def can_run(self, packet):
        return self.__video.can_run(packet) or self.__audio.can_run(packet)

    def run(self, packet):
        if not self.can_run(packet):
            return

        try:
            if self.__video.can_run(packet):
                self.__video.run(packet)

            elif self.__audio.can_run(packet):
                self.__audio.run(packet)

        except Exception as e:
            print('Error on run Video/Audio {}'.format(e))

    def close(self):
        self.__output.close()


class InputStream:
    def __init__(self, filename, video=bool, audio=bool):
        self.input = av.open(filename, 'r')
        self.outputs = list()

        self.can_video = video
        self.can_audio = audio

    def get_stream(self, stream_type):
        return next(s for s in self.input.streams if s.type == stream_type)

    def add_output(self, output):
        self.outputs.append(output)

    def run(self):

        next(self.input.decode(video=0))

        videopackets = []
        audiopackets = []

        for inpacket in self.input.demux():
            if self.can_video and inpacket.stream.type == b'video':
                videopackets.append(inpacket)
                if len(audiopackets) > 0:
                    break

            elif self.can_audio and inpacket.stream.type == b'audio':
                audiopackets.append(inpacket)
                if len(videopackets) > 0:
                    break

        for inpacket in videopackets + audiopackets:
            for output in self.outputs:
                if output.can_run(inpacket):
                    output.run(inpacket)

        for inpacket in self.input.demux():
            for output in self.outputs:
                if output.can_run(inpacket):
                    output.run(inpacket)
