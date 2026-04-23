from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImagesServiceError(_message.Message):
    __slots__ = ()
    class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNSPECIFIED_ERROR: _ClassVar[ImagesServiceError.ErrorCode]
        BAD_TRANSFORM_DATA: _ClassVar[ImagesServiceError.ErrorCode]
        NOT_IMAGE: _ClassVar[ImagesServiceError.ErrorCode]
        BAD_IMAGE_DATA: _ClassVar[ImagesServiceError.ErrorCode]
        IMAGE_TOO_LARGE: _ClassVar[ImagesServiceError.ErrorCode]
        INVALID_BLOB_KEY: _ClassVar[ImagesServiceError.ErrorCode]
        ACCESS_DENIED: _ClassVar[ImagesServiceError.ErrorCode]
        OBJECT_NOT_FOUND: _ClassVar[ImagesServiceError.ErrorCode]
    UNSPECIFIED_ERROR: ImagesServiceError.ErrorCode
    BAD_TRANSFORM_DATA: ImagesServiceError.ErrorCode
    NOT_IMAGE: ImagesServiceError.ErrorCode
    BAD_IMAGE_DATA: ImagesServiceError.ErrorCode
    IMAGE_TOO_LARGE: ImagesServiceError.ErrorCode
    INVALID_BLOB_KEY: ImagesServiceError.ErrorCode
    ACCESS_DENIED: ImagesServiceError.ErrorCode
    OBJECT_NOT_FOUND: ImagesServiceError.ErrorCode
    def __init__(self) -> None: ...

class ImagesServiceTransform(_message.Message):
    __slots__ = ()
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RESIZE: _ClassVar[ImagesServiceTransform.Type]
        ROTATE: _ClassVar[ImagesServiceTransform.Type]
        HORIZONTAL_FLIP: _ClassVar[ImagesServiceTransform.Type]
        VERTICAL_FLIP: _ClassVar[ImagesServiceTransform.Type]
        CROP: _ClassVar[ImagesServiceTransform.Type]
        IM_FEELING_LUCKY: _ClassVar[ImagesServiceTransform.Type]
    RESIZE: ImagesServiceTransform.Type
    ROTATE: ImagesServiceTransform.Type
    HORIZONTAL_FLIP: ImagesServiceTransform.Type
    VERTICAL_FLIP: ImagesServiceTransform.Type
    CROP: ImagesServiceTransform.Type
    IM_FEELING_LUCKY: ImagesServiceTransform.Type
    def __init__(self) -> None: ...

class Transform(_message.Message):
    __slots__ = ("width", "height", "crop_to_fit", "crop_offset_x", "crop_offset_y", "rotate", "horizontal_flip", "vertical_flip", "crop_left_x", "crop_top_y", "crop_right_x", "crop_bottom_y", "autolevels", "allow_stretch", "deprecated_width_set", "deprecated_height_set", "deprecated_crop_offset_x_set", "deprecated_crop_offset_y_set", "deprecated_crop_right_x_set", "deprecated_crop_bottom_y_set")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    CROP_TO_FIT_FIELD_NUMBER: _ClassVar[int]
    CROP_OFFSET_X_FIELD_NUMBER: _ClassVar[int]
    CROP_OFFSET_Y_FIELD_NUMBER: _ClassVar[int]
    ROTATE_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_FLIP_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_FLIP_FIELD_NUMBER: _ClassVar[int]
    CROP_LEFT_X_FIELD_NUMBER: _ClassVar[int]
    CROP_TOP_Y_FIELD_NUMBER: _ClassVar[int]
    CROP_RIGHT_X_FIELD_NUMBER: _ClassVar[int]
    CROP_BOTTOM_Y_FIELD_NUMBER: _ClassVar[int]
    AUTOLEVELS_FIELD_NUMBER: _ClassVar[int]
    ALLOW_STRETCH_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_WIDTH_SET_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_HEIGHT_SET_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_CROP_OFFSET_X_SET_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_CROP_OFFSET_Y_SET_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_CROP_RIGHT_X_SET_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_CROP_BOTTOM_Y_SET_FIELD_NUMBER: _ClassVar[int]
    width: int
    height: int
    crop_to_fit: bool
    crop_offset_x: float
    crop_offset_y: float
    rotate: int
    horizontal_flip: bool
    vertical_flip: bool
    crop_left_x: float
    crop_top_y: float
    crop_right_x: float
    crop_bottom_y: float
    autolevels: bool
    allow_stretch: bool
    deprecated_width_set: bool
    deprecated_height_set: bool
    deprecated_crop_offset_x_set: bool
    deprecated_crop_offset_y_set: bool
    deprecated_crop_right_x_set: bool
    deprecated_crop_bottom_y_set: bool
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ..., crop_to_fit: bool = ..., crop_offset_x: _Optional[float] = ..., crop_offset_y: _Optional[float] = ..., rotate: _Optional[int] = ..., horizontal_flip: bool = ..., vertical_flip: bool = ..., crop_left_x: _Optional[float] = ..., crop_top_y: _Optional[float] = ..., crop_right_x: _Optional[float] = ..., crop_bottom_y: _Optional[float] = ..., autolevels: bool = ..., allow_stretch: bool = ..., deprecated_width_set: bool = ..., deprecated_height_set: bool = ..., deprecated_crop_offset_x_set: bool = ..., deprecated_crop_offset_y_set: bool = ..., deprecated_crop_right_x_set: bool = ..., deprecated_crop_bottom_y_set: bool = ...) -> None: ...

class ImageData(_message.Message):
    __slots__ = ("content", "blob_key", "width", "height", "deprecated_blob_key_set")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    BLOB_KEY_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_BLOB_KEY_SET_FIELD_NUMBER: _ClassVar[int]
    content: bytes
    blob_key: str
    width: int
    height: int
    deprecated_blob_key_set: bool
    def __init__(self, content: _Optional[bytes] = ..., blob_key: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., deprecated_blob_key_set: bool = ...) -> None: ...

class InputSettings(_message.Message):
    __slots__ = ("correct_exif_orientation", "parse_metadata", "transparent_substitution_rgb", "deprecated_correct_exif_orientation_set", "deprecated_transparent_substitution_rgb_set")
    class ORIENTATION_CORRECTION_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNCHANGED_ORIENTATION: _ClassVar[InputSettings.ORIENTATION_CORRECTION_TYPE]
        CORRECT_ORIENTATION: _ClassVar[InputSettings.ORIENTATION_CORRECTION_TYPE]
    UNCHANGED_ORIENTATION: InputSettings.ORIENTATION_CORRECTION_TYPE
    CORRECT_ORIENTATION: InputSettings.ORIENTATION_CORRECTION_TYPE
    CORRECT_EXIF_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    PARSE_METADATA_FIELD_NUMBER: _ClassVar[int]
    TRANSPARENT_SUBSTITUTION_RGB_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_CORRECT_EXIF_ORIENTATION_SET_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_TRANSPARENT_SUBSTITUTION_RGB_SET_FIELD_NUMBER: _ClassVar[int]
    correct_exif_orientation: InputSettings.ORIENTATION_CORRECTION_TYPE
    parse_metadata: bool
    transparent_substitution_rgb: int
    deprecated_correct_exif_orientation_set: bool
    deprecated_transparent_substitution_rgb_set: bool
    def __init__(self, correct_exif_orientation: _Optional[_Union[InputSettings.ORIENTATION_CORRECTION_TYPE, str]] = ..., parse_metadata: bool = ..., transparent_substitution_rgb: _Optional[int] = ..., deprecated_correct_exif_orientation_set: bool = ..., deprecated_transparent_substitution_rgb_set: bool = ...) -> None: ...

class OutputSettings(_message.Message):
    __slots__ = ("mime_type", "quality")
    class MIME_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PNG: _ClassVar[OutputSettings.MIME_TYPE]
        JPEG: _ClassVar[OutputSettings.MIME_TYPE]
        WEBP: _ClassVar[OutputSettings.MIME_TYPE]
    PNG: OutputSettings.MIME_TYPE
    JPEG: OutputSettings.MIME_TYPE
    WEBP: OutputSettings.MIME_TYPE
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    mime_type: OutputSettings.MIME_TYPE
    quality: int
    def __init__(self, mime_type: _Optional[_Union[OutputSettings.MIME_TYPE, str]] = ..., quality: _Optional[int] = ...) -> None: ...

class ImagesTransformRequest(_message.Message):
    __slots__ = ("image", "transform", "output", "input")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    image: ImageData
    transform: _containers.RepeatedCompositeFieldContainer[Transform]
    output: OutputSettings
    input: InputSettings
    def __init__(self, image: _Optional[_Union[ImageData, _Mapping]] = ..., transform: _Optional[_Iterable[_Union[Transform, _Mapping]]] = ..., output: _Optional[_Union[OutputSettings, _Mapping]] = ..., input: _Optional[_Union[InputSettings, _Mapping]] = ...) -> None: ...

class ImagesTransformResponse(_message.Message):
    __slots__ = ("image", "source_metadata")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_METADATA_FIELD_NUMBER: _ClassVar[int]
    image: ImageData
    source_metadata: str
    def __init__(self, image: _Optional[_Union[ImageData, _Mapping]] = ..., source_metadata: _Optional[str] = ...) -> None: ...

class CompositeImageOptions(_message.Message):
    __slots__ = ("source_index", "x_offset", "y_offset", "opacity", "anchor")
    class ANCHOR(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TOP_LEFT: _ClassVar[CompositeImageOptions.ANCHOR]
        TOP: _ClassVar[CompositeImageOptions.ANCHOR]
        TOP_RIGHT: _ClassVar[CompositeImageOptions.ANCHOR]
        LEFT: _ClassVar[CompositeImageOptions.ANCHOR]
        CENTER: _ClassVar[CompositeImageOptions.ANCHOR]
        RIGHT: _ClassVar[CompositeImageOptions.ANCHOR]
        BOTTOM_LEFT: _ClassVar[CompositeImageOptions.ANCHOR]
        BOTTOM: _ClassVar[CompositeImageOptions.ANCHOR]
        BOTTOM_RIGHT: _ClassVar[CompositeImageOptions.ANCHOR]
    TOP_LEFT: CompositeImageOptions.ANCHOR
    TOP: CompositeImageOptions.ANCHOR
    TOP_RIGHT: CompositeImageOptions.ANCHOR
    LEFT: CompositeImageOptions.ANCHOR
    CENTER: CompositeImageOptions.ANCHOR
    RIGHT: CompositeImageOptions.ANCHOR
    BOTTOM_LEFT: CompositeImageOptions.ANCHOR
    BOTTOM: CompositeImageOptions.ANCHOR
    BOTTOM_RIGHT: CompositeImageOptions.ANCHOR
    SOURCE_INDEX_FIELD_NUMBER: _ClassVar[int]
    X_OFFSET_FIELD_NUMBER: _ClassVar[int]
    Y_OFFSET_FIELD_NUMBER: _ClassVar[int]
    OPACITY_FIELD_NUMBER: _ClassVar[int]
    ANCHOR_FIELD_NUMBER: _ClassVar[int]
    source_index: int
    x_offset: int
    y_offset: int
    opacity: float
    anchor: CompositeImageOptions.ANCHOR
    def __init__(self, source_index: _Optional[int] = ..., x_offset: _Optional[int] = ..., y_offset: _Optional[int] = ..., opacity: _Optional[float] = ..., anchor: _Optional[_Union[CompositeImageOptions.ANCHOR, str]] = ...) -> None: ...

class ImagesCanvas(_message.Message):
    __slots__ = ("width", "height", "output", "color", "deprecated_color_set")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_COLOR_SET_FIELD_NUMBER: _ClassVar[int]
    width: int
    height: int
    output: OutputSettings
    color: int
    deprecated_color_set: bool
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ..., output: _Optional[_Union[OutputSettings, _Mapping]] = ..., color: _Optional[int] = ..., deprecated_color_set: bool = ...) -> None: ...

class ImagesCompositeRequest(_message.Message):
    __slots__ = ("image", "options", "canvas")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    CANVAS_FIELD_NUMBER: _ClassVar[int]
    image: _containers.RepeatedCompositeFieldContainer[ImageData]
    options: _containers.RepeatedCompositeFieldContainer[CompositeImageOptions]
    canvas: ImagesCanvas
    def __init__(self, image: _Optional[_Iterable[_Union[ImageData, _Mapping]]] = ..., options: _Optional[_Iterable[_Union[CompositeImageOptions, _Mapping]]] = ..., canvas: _Optional[_Union[ImagesCanvas, _Mapping]] = ...) -> None: ...

class ImagesCompositeResponse(_message.Message):
    __slots__ = ("image",)
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    image: ImageData
    def __init__(self, image: _Optional[_Union[ImageData, _Mapping]] = ...) -> None: ...

class ImagesHistogramRequest(_message.Message):
    __slots__ = ("image",)
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    image: ImageData
    def __init__(self, image: _Optional[_Union[ImageData, _Mapping]] = ...) -> None: ...

class ImagesHistogram(_message.Message):
    __slots__ = ("red", "green", "blue")
    RED_FIELD_NUMBER: _ClassVar[int]
    GREEN_FIELD_NUMBER: _ClassVar[int]
    BLUE_FIELD_NUMBER: _ClassVar[int]
    red: _containers.RepeatedScalarFieldContainer[int]
    green: _containers.RepeatedScalarFieldContainer[int]
    blue: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, red: _Optional[_Iterable[int]] = ..., green: _Optional[_Iterable[int]] = ..., blue: _Optional[_Iterable[int]] = ...) -> None: ...

class ImagesHistogramResponse(_message.Message):
    __slots__ = ("histogram",)
    HISTOGRAM_FIELD_NUMBER: _ClassVar[int]
    histogram: ImagesHistogram
    def __init__(self, histogram: _Optional[_Union[ImagesHistogram, _Mapping]] = ...) -> None: ...

class ImagesGetUrlBaseRequest(_message.Message):
    __slots__ = ("blob_key", "create_secure_url")
    BLOB_KEY_FIELD_NUMBER: _ClassVar[int]
    CREATE_SECURE_URL_FIELD_NUMBER: _ClassVar[int]
    blob_key: str
    create_secure_url: bool
    def __init__(self, blob_key: _Optional[str] = ..., create_secure_url: bool = ...) -> None: ...

class ImagesGetUrlBaseResponse(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class ImagesDeleteUrlBaseRequest(_message.Message):
    __slots__ = ("blob_key",)
    BLOB_KEY_FIELD_NUMBER: _ClassVar[int]
    blob_key: str
    def __init__(self, blob_key: _Optional[str] = ...) -> None: ...

class ImagesDeleteUrlBaseResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
