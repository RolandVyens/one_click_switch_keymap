bl_info = {
    "name": "Keymap Switcher",
    "description": "一键切换原生和行业兼容快捷键",
    "author": "Roland Vyens",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "category": "System",
    "doc_url": "https://github.com/RolandVyens?tab=repositories",
}


import bpy
import os


bl_path = os.getcwd()
runtime_folder = os.listdir()
bl_versionfolder = runtime_folder[0]
blender_keymap = str(
    f"{bl_path}\\{bl_versionfolder}\\scripts\\presets\\keyconfig\\Blender.py"
)
industry_keymap = str(
    f"{bl_path}\\{bl_versionfolder}\\scripts\\presets\\keyconfig\\Industry_Compatible.py"
)
buttonlanguage = {"default": "Switch KeyMap", "zh_CN": "切换键位"}
currentlanguage = bpy.app.translations.locale


def Switch_keymaps():
    active_keymap = bpy.context.preferences.keymap.active_keyconfig

    if active_keymap == "Blender":
        bpy.ops.preferences.keyconfig_activate(filepath=industry_keymap)
        active_keymap = bpy.context.preferences.keymap.active_keyconfig
        info = f"{active_keymap} 行业兼容键位"

    elif active_keymap == "Industry_Compatible":
        bpy.ops.preferences.keyconfig_activate(filepath=blender_keymap)
        active_keymap = bpy.context.preferences.keymap.active_keyconfig
        info = f"{active_keymap} 默认键位"

    else:
        active_keymap = "检测到自定义键位，无法切换 (Custom Keymap Detected)"
        info = active_keymap

    return info


class Switch_Keymaps_Button(bpy.types.Operator):
    bl_idname = "preferences.switch_keymaps_button"
    bl_label = buttonlanguage.get(currentlanguage, "Switch KeyMap")
    bl_description = "一键切换bl默认键位或行业兼容键位"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        active_keymap = Switch_keymaps()
        self.report({"INFO"}, f"{active_keymap}")
        return {"FINISHED"}


# def draw_func(self, context):
#     layout = self.layout
#     layout.operator(Switch_Keymaps_Button.bl_idname)


class SwitchKeymapTopbarHeader(bpy.types.Panel):
    bl_label = "Switch Keymap Topbar Header"
    bl_idname = "PT_SwitchKeymapTopbarHeader"
    bl_space_type = "TOPBAR"
    bl_region_type = "HEADER"

    def draw(self, context):
        layout = self.layout

        # Add your operator button
        if context.region.alignment != "RIGHT":
            layout.operator(Switch_Keymaps_Button.bl_idname)


def register():
    bpy.utils.register_class(Switch_Keymaps_Button)
    bpy.utils.register_class(SwitchKeymapTopbarHeader)
    bpy.types.TOPBAR_HT_upper_bar.append(SwitchKeymapTopbarHeader.draw)
    # bpy.types.TOPBAR_HT_upper_bar.append(draw_func)


def unregister():
    bpy.utils.unregister_class(Switch_Keymaps_Button)
    bpy.utils.unregister_class(SwitchKeymapTopbarHeader)
    bpy.types.TOPBAR_HT_upper_bar.remove(SwitchKeymapTopbarHeader.draw)
    # bpy.types.TOPBAR_HT_upper_bar.remove(draw_func)


if __name__ == "__main__":
    register()
