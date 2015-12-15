import json
from pyrope.frame import Frame, FrameParsingError
from pyrope.netstream_property_mapping import PropertyMapper
from pyrope.utils import reverse_bytewise
import sys

'''
Serialization Structure for Frame as follows:
{
 FrameID: {
           CurrentTime: Float,
           DeltaTime: Float,
           Actors: {
                    Shortname: {
                                actorId: Int,
                                actor_type: FullType,
                                new: boolean,
                                open: boolean,
                                startpos: int,
                                data: Array[{
                                             property_id: int,
                                             property_name: str,
                                             property_value: ArrayOfDifferentDataTypes
                                            }]
                                }
                    }
           }
}
'''


class NetstreamParsingError(Exception):
    pass


class Netstream:
    def __init__(self, netstream):
        self._netstream = reverse_bytewise(netstream)
        self.frames = None
        self._toolbar_width = 50

    def parse_frames(self, framenum, objects, netcache):
        self.frames = {}

        sys.stdout.write("[%s]" % (" " * self._toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (self._toolbar_width+1))
        update_bar_each = framenum//self._toolbar_width

        propertymapper = PropertyMapper(netcache)
        for i in range(framenum):
            frame = Frame()
            try:
                frame.parse_frame(self._netstream, objects, propertymapper)
            except FrameParsingError as e:
                e.args += ({"LastFrameActors": self.frames[i-1].actors},)
                raise e
            self.frames[i] = frame

            if i % update_bar_each == 0:
                sys.stdout.write("-")
                sys.stdout.flush()
        sys.stdout.write("\n")
        remaining = self._netstream.read(self._netstream.length-self._netstream.pos)
        remaining.bytealign()
        if remaining.int != 0:
            raise NetstreamParsingError("There seems to be meaningful data left in the Netstream", remaining.hex)
        return self.frames

    def get_movement(self, actor=None):
        if actor:
            pass
        else:
            pass

    def get_actor_list(self):
        return self.frames[0].actor_appeared

    def to_json(self, skip_empty=True):
        def nonempty(x):
            frames = {}
            for k, v in self.frames.items():
                if v.actors:
                    frames[k] = v.__dict__
            return frames
        if skip_empty:
            return json.dumps(self, default=nonempty, sort_keys=True, indent=2)
        return json.dumps(self, default=lambda o: {k:v.__dict__ for k,v in self.frames.items()}, sort_keys=True, indent=2)