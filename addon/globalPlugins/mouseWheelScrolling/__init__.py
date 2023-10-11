#__init__.py
# Copyright (C) 2023 Beka Gozalishvili <beqaprogger@gmail.com>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import addonHandler
import globalPluginHandler
import mouseHandler
from scriptHandler import script
import tones
import winUser

_curAddon = addonHandler.getCodeAddon()
addonName = _curAddon.name
_addonSummary = _curAddon.manifest['summary']
addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    MAX_AMOUNT = 500
    scriptCategory = _addonSummary

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enabled = False
        self.standard_gestures = {"kb:nvda+shift+control+w": "toggleMouseWheel"}
        self.gestures = {"kb:leftArrow": "scrollLeft", "kb:rightArrow": "scrollRight", "kb:upArrow": "scrollUp", "kb:downArrow": "scrollDown", "kb:pageup": "scrollUpPage", "kb:pagedown": "scrollDownPage", "kb:home": "scrollMax", "kb:end": "scrollMin"}
        self.set_standard_gestures()

    def scrollTo(self, amount, isVertical=True):
        scrollEvent = winUser.MOUSEEVENTF_WHEEL if isVertical else winUser.MOUSEEVENTF_HWHEEL
        sign = -1 if amount < 0 else 1
        quotient, reminder = divmod(abs(amount), self.MAX_AMOUNT)
        for i in range(quotient + 1):
            scrollAmount = sign *self.MAX_AMOUNT if i < quotient else sign * reminder
            if scrollAmount != 0:
                mouseHandler.executeMouseEvent(scrollEvent, 0, 0, scrollAmount)

    @script(description=_("Scrolls up an object under the mouse cursor"))
    def script_scrollUp(self, gesture):
        self.scrollTo(50)

    @script(description=_("Scrolls down an object under the mouse cursor"))
    def script_scrollDown(self, gesture):
        self.scrollTo(-50)

    @script(description=_("Scrolls left an object under the mouse cursor"))
    def script_scrollLeft(self, gesture):
        self.scrollTo(-50, False)

    @script(description=_("Scrolls right an object under the mouse cursor"))
    def script_scrollRight(self, gesture):
        self.scrollTo(50, False)

    @script(description=_("Scrolls up page of an object under the mouse cursor"))
    def script_scrollUpPage(self, gesture):
        self.scrollTo(500)

    @script(description=_("Scrolls down page of an object under the mouse cursor"))
    def script_scrollDownPage(self, gesture):
        self.scrollTo(-500)

    @script(description=_("Tries to scroll an object to the maximum point. Especially usable for sliders"))
    def script_scrollMax(self, gesture):
        self.scrollTo(15000)

    @script(description=_("Tries to scroll an object to the minimum point. Especially usable for sliders"))
    def script_scrollMin(self, gesture):
        self.scrollTo(-15000)

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
