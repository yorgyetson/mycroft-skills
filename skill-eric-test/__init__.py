# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

from .obstest import (streamStatus, startStream, stopStream, startRecording, stopRecording,
    displayEnable)
import asyncio
import json

from mycroft.util.log import getLogger
LOGGER = getLogger(__name__)

class OBSControl(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(OBSControl, self).__init__(name="OBSControl")
        # Initialize working variables used within the skill.
        self.loop = None #asyncio.new_event_loop()

    @intent_handler(IntentBuilder("").require("Stream").require("Start").optionally("Scene"))
    def handle_stream_start_intent(self, message):
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(startStream())
        self.loop.close()
        self.loop = None

        self.speak_dialog("live.stream.started")

    @intent_handler(IntentBuilder("").require("End").require("Stream"))
    def handle_stream_end_intent(self, message):
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(stopStream())
        self.loop.close()
        self.loop = None

        self.speak_dialog("live.stream.ended")

    @intent_handler(IntentBuilder("").require("Start").require("Stream").require("Recording"))
    def handle_stream_recording_start_intent(self, message):
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(startRecording())
        self.loop.close()
        self.loop = None

        self.speak_dialog("stream.recording.started")

    @intent_handler(IntentBuilder("").require("End").require("Stream").require("Recording"))
    def handle_stream_recording_end_intent(self, message):
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(stopRecording())
        self.loop.close()
        self.loop = None

        self.speak_dialog("stream.recording.ended")


    @intent_handler(IntentBuilder("").require("Stream").require("Status"))
    def handle_stream_status_intent(self, message):
        self.loop = asyncio.new_event_loop()
        response = self.loop.run_until_complete(streamStatus())

        if response.streaming == True:
            streaming = "live"
        else:
            streaming = "not broadcasting"

        if response.recording == True:
            recording = "recording"
        else:
            recording = "not recording"

        self.loop.close()
        self.loop = None
        self.speak_dialog("stream.status", {"recording": recording,
                                            "streaming": streaming})


    def stop(self):
        return False


def create_skill():
    return OBSControl()
