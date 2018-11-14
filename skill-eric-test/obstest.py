"""Example shows how to send requests and get responses."""

import asyncio

from obswsrc import OBSWS
from obswsrc.requests import (ResponseStatus, GetStreamingStatusRequest,
    StartStreamingRequest, StopStreamingRequest, StartRecordingRequest,
    StopRecordingRequest, GetCurrentSceneRequest, SetSourceRenderRequest)
from obswsrc.types import Stream, StreamSettings


async def displayEnable():

    async with OBSWS('192.168.0.4', 4444, "password") as obsws:

        # We can send an empty StartStreaming request (in that case the plugin
        # will use OBS configuration), but let's provide some settings as well
        #stream_settings = StreamSettings(
        #    server="rtmp://example.org/my_application",
        #    key="secret_stream_key",
        #    use_auth=False
        #)
        stream = Stream(
            #settings=stream_settings,
            type="rtmp_custom",
        )

        # Now let's actually perform a request
        # response = await obsws.require(StartStreamingRequest(stream=stream))
        response = await obsws.require(GetCurrentSceneRequest())

        # Check if everything is OK
        if response.status == ResponseStatus.OK:
            print(response)
            for source in response.sources:
                source_response = await obsws.require(SetSourceRenderRequest({"source": source.name,
                                                                              "render": True}))
                if source_response.status == ResponseStatus.OK:
                    pass
                else:
                    print(response.error)
        else:
         print(response.error)


async def startStream():

    async with OBSWS('192.168.0.4', 4444, "password") as obsws:

        stream = Stream(
            type="rtmp_custom",
        )

        response = await obsws.require(StartStreamingRequest(stream=stream))

        # Check if everything is OK
        if response.status == ResponseStatus.OK:
            print("success")
        else:
            print(response.error)


async def stopStream():

    async with OBSWS('192.168.0.4', 4444, "password") as obsws:

        stream = Stream(
            type="rtmp_custom",
        )

        response = await obsws.require(StopStreamingRequest())

        # Check if everything is OK
        if response.status == ResponseStatus.OK:
            print("success")
        else:
            print(response.error)


async def startRecording():

    async with OBSWS('192.168.0.4', 4444, "password") as obsws:

        stream = Stream(
            type="rtmp_custom",
        )

        response = await obsws.require(StartRecordingRequest())

        # Check if everything is OK
        if response.status == ResponseStatus.OK:
            print("success")
        else:
            print(response.error)


async def stopRecording():

    async with OBSWS('192.168.0.4', 4444, "password") as obsws:

        stream = Stream(
            type="rtmp_custom",
        )

        response = await obsws.require(StopRecordingRequest())

        # Check if everything is OK
        if response.status == ResponseStatus.OK:
            print("success")
        else:
            print(response.error)


async def streamStatus():

    async with OBSWS('192.168.0.4', 4444, "password") as obsws:

        stream = Stream(
            type="rtmp_custom",
        )

        response = await obsws.require(GetStreamingStatusRequest())

        # Check if everything is OK
        if response.status == ResponseStatus.OK:
            return response
        else:
            print(response.error)
            return response

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(displayEnable())
    loop.close()
