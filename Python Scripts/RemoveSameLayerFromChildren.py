from typing import Iterator, Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected


def iter_descendants(parent: c4d.BaseObject) -> Iterator[c4d.BaseObject]:
    """Yields all children, grandchildren, etc. of parent (not parent itself)."""
    stack = []
    child = parent.GetDown()
    while child is not None:
        stack.append(child)
        child = child.GetNext()
    while stack:
        obj = stack.pop()
        yield obj
        child = obj.GetDown()
        while child is not None:
            stack.append(child)
            child = child.GetNext()


def remove_layer_from_children() -> None:
    # Top-most selected objects only; a selected child is covered by its selected parent.
    objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_NONE)
    if not objects:
        return

    doc.StartUndo()

    for parent in objects:
        layer = parent.GetLayerObject(doc)
        if layer is None:
            continue  # No layer on this object -> leave its children alone

        for child in iter_descendants(parent):
            if child.GetLayerObject(doc) == layer:  # Only children on the same layer
                doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, child)
                child.SetLayerObject(None)

    doc.EndUndo()
    c4d.EventAdd()


if __name__ == '__main__':
    remove_layer_from_children()
