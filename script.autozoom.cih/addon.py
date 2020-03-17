
import sys
import xbmcgui
import xbmcaddon
import xbmc
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
ASPECT_RATIO_TO_ZOOM = ["1.33", "1.37", "1.66", "1.78", "1.85"]


def getAspectRatio(xbmc):
    return xbmc.getInfoLabel('VideoPlayer.VideoAspect')


def setMasking(xbmc):
    xbmc.executebuiltin('skin.reset (scopemask)')
    xbmc.executebuiltin('Skin.setbool (ARmask)')


ZOOM_LEVEL = 23


def setZoomNonScope(xbmc):
    # need to zoom out to 77
    for _level in range(ZOOM_LEVEL):
        xbmc.executebuiltin('XBMC.Action(ZoomOut)')


def resetZoom(xbmc):
    for _level in range(ZOOM_LEVEL):
        xbmc.executebuiltin('XBMC.Action(ZoomIn)')


def main(xbmc):
    xbmc.log('addon %s starting' % addonname)
    try:
        aspect_ratio = getAspectRatio(xbmc)
        xbmc.log('aspect ratio: %s' % aspect_ratio)
        should_zoom = getAspectRatio(xbmc) in ASPECT_RATIO_TO_ZOOM
        xbmc.log('should zoom: %s' % should_zoom)
        if sys.argv[1] == 'zoom' and should_zoom:
            xbmc.log('attempting to zoom')
            setZoomNonScope(xbmc)
        if sys.argv[1] == 'reset' and should_zoom:
            xbmc.log('attempting to reset')
            setZoomNonScope(xbmc)
    except:
        xbmc.log("Unexpected error: %s" % sys.exc_info()[0])


if __name__ == '__main__':
    main(xbmc)
