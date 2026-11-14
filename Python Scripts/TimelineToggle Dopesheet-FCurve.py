from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

# Timeline mode command IDs from the Script Log.
DOPE_SHEET_MODE_ID = 465001191
F_CURVE_MODE_ID = 465001190
MOTION_MODE_ID = 465001193


def timeline_mode_toggle() -> None:
    if c4d.IsCommandChecked(DOPE_SHEET_MODE_ID):
        c4d.CallCommand(F_CURVE_MODE_ID)       # Dope Sheet -> F-Curve
    elif c4d.IsCommandChecked(F_CURVE_MODE_ID) or c4d.IsCommandChecked(MOTION_MODE_ID):
        c4d.CallCommand(DOPE_SHEET_MODE_ID)    # F-Curve or Motion -> Dope Sheet
    # No mode active (no Timeline active) -> do nothing

    c4d.EventAdd()


if __name__ == '__main__':
    timeline_mode_toggle()