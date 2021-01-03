import math
import os
import pathlib
from typing import List, Optional, Tuple

from PIL import Image


class Collection:
    def __init__(self, path: pathlib.PosixPath):
        self.name = path.name
        self.image_paths = []
        self.preview_path = path.parent / "preview.jpg"
        for image_path in sorted([
            x
            for x in path.glob("./*")
            if x.is_file()
            and any(str(x).endswith(ext) for ext in [".png", ".jpg", ".jpeg"])
        ]):
            if image_path.name.startswith("preview"):
                self.preview_path = image_path
            else:
                self.image_paths.append(image_path)
        self.num_items = len(self.image_paths)
        self.image_width, self.image_height = self._validate_image_dimensions()
        self.images_per_row = math.ceil(math.sqrt(self.num_items))
        self.images_per_column = (
            math.floor(self.num_items / self.images_per_row)
            if self.num_items % self.images_per_row == 0
            else math.ceil(self.num_items / self.images_per_row)
        )

    def _validate_image_dimensions(self) -> Tuple[int, int]:
        """ Checks that all images in input paths have same dimensions

        Returns:
            (width, height) if successful
        Raises:
            AssertionError if widths and heights of images are not identical
        """
        with Image.open(self.image_paths[0]) as img:
            width, height = img.size
        try:
            for image_path in self.image_paths[1:]:
                with Image.open(image_path) as img:
                    temp_width, temp_height = img.size
                    assert width == temp_width
                    assert height == temp_height
        except AssertionError:
            print(self.image_paths[0])
            print(width, height)
            print(image_path)
            print(temp_width, temp_height)
            raise
        return width, height


class CollectionFactory:
    _collection_registry = {}

    def __init__(self):
        dir_path = pathlib.Path(__file__).parent.absolute() / "files"
        for subdir in [
            x for x in dir_path.iterdir() if x.is_dir() and not x.name.startswith("__")
        ]:
            self._collection_registry[subdir.name] = Collection(subdir)

    def get_collection(self, collection_name: str) -> Optional[Collection]:
        if collection_name in self._collection_registry:
            return self._collection_registry[collection_name]
        else:
            return None


collections = CollectionFactory()


def get_collections():
    return sorted(list(collections._collection_registry.keys()))


def get_collection(collection_name: str):
    return collections.get_collection(collection_name)
