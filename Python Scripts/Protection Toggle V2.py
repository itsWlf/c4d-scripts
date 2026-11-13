from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected


def has_protection_tag(obj: c4d.BaseObject) -> bool:
    """Returns True if the object carries at least one Protection tag."""
    return obj.GetTag(c4d.Tprotection) is not None


def protectiontagtoggle() -> None:
    # All selected objects, including selected children of selected objects.
    objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not objects:
        return

    doc.StartUndo()

    if all(has_protection_tag(obj) for obj in objects):
        # Every selected object is protected -> remove the tags from all of them.
        for obj in objects:
            tag = obj.GetTag(c4d.Tprotection)
            while tag is not None:  # Also clears duplicate Protection tags
                doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, tag)
                tag.Remove()
                tag = obj.GetTag(c4d.Tprotection)
    else:
        # None or only some are protected -> add a tag where it is missing.
        for obj in objects:
            if not has_protection_tag(obj):
                tag = obj.MakeTag(c4d.Tprotection)
                if tag is not None:
                    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, tag)

    doc.EndUndo()
    c4d.EventAdd()


if __name__ == '__main__':
    protectiontagtoggle()
