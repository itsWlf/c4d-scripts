from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected


def remove_empty_material_tags() -> None:
    # All selected objects, including selected children of selected objects.
    objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not objects:
        return

    doc.StartUndo()

    for obj in objects:
        # Collect first, then remove, so the tag list isn't changed while looping over it.
        empty_tags = [
            tag for tag in obj.GetTags()
            if tag.GetType() == c4d.Ttexture and tag.GetMaterial() is None
        ]
        for tag in empty_tags:
            doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, tag)
            tag.Remove()

    doc.EndUndo()
    c4d.EventAdd()


if __name__ == '__main__':
    remove_empty_material_tags()