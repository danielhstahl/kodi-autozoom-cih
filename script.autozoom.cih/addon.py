
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


def setZoomNonScope(xbmc):
    # need to zoom out to 77
    zoomlevel = 8
    for _level in range(zoomlevel):
        xbmc.executebuiltin('XBMC.Action(ZoomOut)')


def resetZoom(xbmc):
    zoomlevel = 8
    for _level in range(zoomlevel):
        xbmc.executebuiltin('XBMC.Action(ZoomIn)')


def main(xbmc):
    xbmc.log('addon %s starting' % addonname,  xbmc.LOGDEBUG)
    try:
        should_zoom = getAspectRatio(xbmc) in ASPECT_RATIO_TO_ZOOM
        xbmc.log('should zoom: %s' % should_zoom,  xbmc.LOGDEBUG)
        if sys.argv[1] == 'zoom' and should_zoom:
            xbmc.log('attempting to zoom',  xbmc.LOGDEBUG)
            setZoomNonScope(xbmc)
        if sys.argv[1] == 'reset' and should_zoom:
            xbmc.log('attempting to reset',  xbmc.LOGDEBUG)
            setZoomNonScope(xbmc)
    except:
        xbmc.log("Unexpected error: %s" % sys.exc_info()[0], xbmc.LOGDEBUG)


if __name__ == '__main__':
    main(xbmc)
