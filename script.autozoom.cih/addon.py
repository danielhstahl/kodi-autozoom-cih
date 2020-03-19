
import sys
import xbmcgui
import xbmcaddon
import xbmc
import json
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
capture = xbmc.RenderCapture()
ASPECT_RATIO_TO_ZOOM = ["1.33", "1.37", "1.66", "1.78", "1.85"]

# capture Width & Height
# each captured pixel is 40wx20h of the screen pixel
# 1920 x 1080 = 1.77
# 1920 x 1038 = 1.85 (20) (line 0 dark)
# 1920 x 960 = 2.0 (60) (line 0 - 2 dark)
# 1920 x 817 = 2.35 (130) (line 0 - 5 dark)
CAPTURE_WIDTH = 48
CAPTURE_HEIGHT = 54


def CaptureFrame(xbmc, capture):
    capture.capture(CAPTURE_WIDTH, CAPTURE_HEIGHT,
                    xbmc.CAPTURE_FLAG_CONTINUOUS)

    while (capture.getCaptureState() != xbmc.CAPTURE_STATE_DONE):
        capture.waitForCaptureStateChangeEvent()

        if (capture.getCaptureState() == xbmc.CAPTURE_STATE_DONE):
            capturedImage = capture.getImage()
            return capturedImage


def LineColorLessThan(_bArray, _lineStart, _lineCount, _threshold):
    __sliceStart = _lineStart * CAPTURE_WIDTH * 4
    __sliceEnd = (_lineStart + _lineCount) * CAPTURE_WIDTH * 4

    # zero out the alpha channel
    i = __sliceStart + 3
    while (i < __sliceEnd):
        _bArray[i] &= 0x00
        i += 4

    __imageLine = _bArray[__sliceStart:__sliceEnd]
    return all([v < _threshold for v in __imageLine])


def GetAspectRatioFromFrame(xbmc, capture):
    __aspectratio = capture.getAspectRatio()
    __threshold = 25
    xbmcAspectRatio = xbmc.getInfoLabel('VideoPlayer.VideoAspect')
    # Analyze the frame only if the ratio is 16:9. 2.35 ratio files
    # would not have black bars hardcoded.
    if 1.40 < __aspectratio < 1.80:
        # screen capture and test for an image that is not dark in the 2.40
        # aspect ratio area. keep on capturing images until captured image
        # is not dark
        while (True):
            __myimage = CaptureFrame(xbmc, capture)
            __middleScreenDark = LineColorLessThan(
                __myimage, 7, 2, __threshold)
            if __middleScreenDark == False:
                xbmc.sleep(200)
                break
            else:
                xbmc.sleep(100)

        # Capture another frame. after we have waited for transitions
        __myimage = CaptureFrame(xbmc, capture)
        __ar185 = LineColorLessThan(__myimage, 0, 1, __threshold)
        __ar200 = LineColorLessThan(__myimage, 1, 3, __threshold)
        __ar235 = LineColorLessThan(__myimage, 1, 5, __threshold)

        if (__ar235 == True):
            xbmcAspectRatio = "2.35"

        elif (__ar200 == True):
            xbmcAspectRatio = "2.00"

        elif (__ar185 == True):
            xbmcAspectRatio = "1.85"
    return xbmcAspectRatio


def setMasking(xbmc):
    xbmc.executebuiltin('skin.reset (scopemask)')
    xbmc.executebuiltin('Skin.setbool (ARmask)')


ZOOM_LEVEL = 23
ZOOM_RESET = 50


def _zoomHelper(zoom_level):
    return {
        "jsonrpc": "2.0",
        "method": "Player.SetViewMode",
        "params": {"viewmode": {"zoom": zoom_level}},
        "id": 1
    }


def setZoomNonScope(xbmc):
    # need to zoom out to 76
    body = _zoomHelper(.76)
    json_response = xbmc.executeJSONRPC(json.dumps(body).encode("utf-8"))
    #json_object = json.loads(json_response.decode('utf-8', 'replace'))
    xbmc.log("Response: %s" % json_response)


def resetZoom(xbmc):
    body = _zoomHelper(1)
    json_response = xbmc.executeJSONRPC(json.dumps(body).encode("utf-8"))
    xbmc.log("Reset Zoom")
    xbmc.log("Response: %s" % json_response)
    #json_object = json.loads(json_response.decode('utf-8', 'replace'))
    #xbmc.log("Response: %s" % json_object)


def main(xbmc):
    xbmc.log('addon %s starting' % addonname)

    # try:
    resetZoom(xbmc)
    aspect_ratio = GetAspectRatioFromFrame(xbmc, capture)
    xbmc.log('aspect ratio: %s' % aspect_ratio)
    should_zoom = aspect_ratio in ASPECT_RATIO_TO_ZOOM
    xbmc.log('should zoom: %s' % should_zoom)
    if should_zoom:
        xbmc.log('attempting to zoom')
        setZoomNonScope(xbmc)
    # except:
    #    xbmc.log("Unexpected error: %s" % sys.exc_info()[0])


if __name__ == '__main__':
    main(xbmc)
