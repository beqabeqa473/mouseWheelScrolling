#__init__.py
# Copyright (C) 2023 Beka Gozalishvili <beqaprogger@gmail.com>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import globalPluginHandler
import mouseHandler
from scriptHandler import script
import tones
import winUser

_curAddon = addonHandler.getCodeAddon()
addonName = _curAddon.name.lower()
_addonSummary = _curAddon.manifest['summary']
addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _addonSummary

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enabled = False
        self.standard_gestures = {"kb:nvda+shift+control+w": "toggleMouseWheel"}
        self.gestures = {"kb:leftArrow": "scrollLeft", "kb:rightArrow": "scrollRight", "kb:upArrow": "scrollUp", "kb:downArrow": "scrollDown", "kb:pageup": "scrollUpPage", "kb:pagedown": "scrollDownPage", "kb:home": "scrollMax", "kb:end": "scrollMin"}
        self.set_standard_gestures()

    def getDirection(self, gesture):
        direction = gesture.mainKeyName[0]
        return direction

    def scrollTo(self, gesture, amount):
        direction = self.getDirection(gesture)
        scrollEvent = winUser.MOUSEEVENTF_WHEEL if direction in ["u", "d"] else winUser.MOUSEEVENTF_HWHEEL
        mouseHandler.executeMouseEvent(scrollEvent, 0, 0, amount)

    def scrollBatched(self, gesture, amount):
        for i in range(20):
            self.scrollTo(gesture, amount)

    @script(description=_("Scrolls up an object under the mouse cursor"))
    def script_scrollUp(self, gesture):
        self.scrollTo(gesture, 50)

    @script(description=_("Scrolls down an object under the mouse cursor"))
    def script_scrollDown(self, gesture):
        self.scrollTo(gesture, -50)

    @script(description=_("Scrolls left an object under the mouse cursor"))
    def script_scrollLeft(self, gesture):
        self.scrollTo(gesture, -50)

    @script(description=_("Scrolls right an object under the mouse cursor"))
    def script_scrollRight(self, gesture):
        self.scrollTo(gesture, 50)

    @script(description=_("Scrolls up page of an object under the mouse cursor"))
    def script_scrollUpPage(self, gesture):
        self.scrollTo(gesture, 500)

    @script(description=_("Scrolls down page of an object under the mouse cursor"))
    def script_scrollDownPage(self, gesture):
        self.scrollTo(gesture, -500)

    @script(description=_("Tries to scroll an object to the maximum point. Especially usable for sliders"))
    def script_scrollMax(self, gesture):
        self.scrollBatched(gesture, 500)

    @script(description=_("Tries to scroll an object to the minimum point. Especially usable for sliders"))
    def script_scrollMin(self, gesture):
        self.scrollBatched(gesture, -500)

    @script(description=_("toggles a mode of scrolling with mouse wheel"))
    def script_toggleMouseWheel(self, gesture):
        self.enabled = not self.enabled
        if not self.enabled:
            tones.beep(440, 100)
            self.set_standard_gestures()
            return
        tones.beep(880, 100)
        self.set_all_gestures()

    def set_standard_gestures(self):
        self.clearGestureBindings()
        self.bindGestures(self.standard_gestures)

    def set_all_gestures(self):
        self.clearGestureBindings()
        self.bindGestures(self.standard_gestures)
        self.bindGestures(self.gestures)
