import os
from enum import Enum

from gi.repository import Gtk, Gio, GLib, GdkPixbuf


WIDGET_SPACING = 10


class IconsNames(Enum):
    HOME = 'user-home'
    DESKTOP = 'user-desktop'
    FILE_MANAGER = 'system-file-manager'


class IconThemePreview(Gtk.ListBox):

    icons_plugin_name = None

    icons_templates = None
    icons_imageboxes = None

    def __init__(self):
        self.icons_imageboxes = {}
        self.icons_templates = {}
        super().__init__()
        self.set_margin_left(WIDGET_SPACING)
        self.set_margin_right(WIDGET_SPACING)

        # self.bg = Gtk.Grid(row_spacing=6, column_spacing=6)
        # self.bg.set_margin_top(WIDGET_SPACING/2)
        # self.bg.set_margin_bottom(WIDGET_SPACING)

        self.set_selection_mode(Gtk.SelectionMode.NONE)
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row.add(hbox)
        for icon in IconsNames:
            icon_imagebox = Gtk.Image()
            hbox.pack_start(icon_imagebox, True, True, 0)
            self.icons_imageboxes[icon.name] = icon_imagebox
        self.add(row)
        self.show_all()

    def update_preview(self, colorscheme, theme_plugin):
        transform_function = theme_plugin.preview_transform_function
        self.load_icon_templates(theme_plugin)
        for icon in IconsNames:
            source_image = self.icons_templates[icon.name]
            target_imagebox = self.icons_imageboxes[icon.name]
            new_svg_image = transform_function(
                source_image, colorscheme
            ).encode('ascii')
            stream = Gio.MemoryInputStream.new_from_bytes(
                GLib.Bytes.new(new_svg_image)
            )

            # @TODO: is it possible to make it faster?
            pixbuf = GdkPixbuf.Pixbuf.new_from_stream(stream, None)

            target_imagebox.set_from_pixbuf(pixbuf)

    def load_icon_templates(self, theme_plugin):
        if theme_plugin.name == self.icons_plugin_name:
            return
        self.icons_plugin_name = theme_plugin.name
        for icon in IconsNames:
            template_path = "{}.svg.template".format(icon.value)
            with open(
                os.path.join(
                    theme_plugin.preview_svg_dir, template_path
                ), "rb"
            ) as file_object:
                self.icons_templates[icon.name] = file_object.read().decode('utf-8')
