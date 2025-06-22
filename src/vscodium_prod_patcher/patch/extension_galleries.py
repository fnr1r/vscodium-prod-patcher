# pylint: disable=line-too-long

EXTENSIONS_OPENVSX_GALLERY = {
    "serviceUrl": "https://open-vsx.org/vscode/gallery",
    "itemUrl": "https://open-vsx.org/vscode/item",
    "extensionUrlTemplate": "https://open-vsx.org/vscode/gallery/{publisher}/{name}/latest",  # noqa: E501
    "controlUrl": "https://raw.githubusercontent.com/EclipseFdn/publish-extensions/refs/heads/master/extension-control/extensions.json",  # noqa: E501
}
EXTENSIONS_OPENVSX_TRUSTED = ["https://open-vsx.org"]

EXTENSIONS_MS_GALLERY = {
    "serviceUrl": "https://marketplace.visualstudio.com/_apis/public/gallery",
    "cacheUrl": "https://vscode.blob.core.windows.net/gallery/index",
    "itemUrl": "https://marketplace.visualstudio.com/items",
}
