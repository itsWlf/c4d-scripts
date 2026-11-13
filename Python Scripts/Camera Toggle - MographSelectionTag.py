# Camera Toggle shortcut that uses the mograph selection tag as the indicator of what camera to activate.
from typing import Iterator, Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

# Object types that count as cameras: standard Camera and Redshift Camera.
CAMERA_TYPES = {c4d.Ocamera, c4d.Orscamera}


def iter_all_objects(obj: Optional[c4d.BaseObject]) -> Iterator[c4d.BaseObject]:
    """Walks the whole object hierarchy top to bottom, like the Object Manager."""
    while obj is not None:
        yield obj
        if obj.GetDown() is not None:
            obj = obj.GetDown()
            continue
        while obj is not None and obj.GetNext() is None:
            obj = obj.GetUp()
        if obj is not None:
            obj = obj.GetNext()


def find_tagged_camera() -> Optional[c4d.BaseObject]:
    """Returns the first camera in the Object Manager that carries a MoGraph Selection tag."""
    for obj in iter_all_objects(doc.GetFirstObject()):
        if obj.GetType() in CAMERA_TYPES and obj.GetTag(c4d.Tmgselection) is not None:
            return obj
    return None


def tagged_camera_toggle() -> None:
    bd = doc.GetActiveBaseDraw()  # The currently selected viewport
    if bd is None:
        return

    tagged_cam = find_tagged_camera()
    if tagged_cam is None:
        return  # No camera with a MoGraph Selection tag -> do nothing

    # Record the current view state so the switch can be reverted with Undo View (Ctrl+Shift+Z).
    bd.InitUndo(doc)

    current_cam = bd.GetSceneCamera(doc)
    if current_cam == tagged_cam:
        # Already looking through that camera -> back to the default editor camera.
        bd.SetSceneCamera(bd.GetEditorCamera())
    else:
        # Editor camera or any other camera -> switch to that camera.
        bd.SetSceneCamera(tagged_cam)

    c4d.EventAdd()


if __name__ == '__main__':
    tagged_camera_toggle()
