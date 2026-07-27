import bpy
import rna_keymap_ui

# Blenderが対応している主要言語の網羅リスト
LANG_ITEMS = [
    ('en_US', 'English', 'English'),
    ('ja_JP', 'Japanese', 'Japanese'),
    ('es', 'Spanish', 'Spanish'),
    ('fr_FR', 'French', 'French'),
    ('de_DE', 'German', 'German'),
    ('it_IT', 'Italian', 'Italian'),
    ('pt_PT', 'Portuguese', 'Portuguese'),
    ('pt_BR', 'Portuguese (Brazil)', 'Portuguese (Brazil)'),
    ('es_ES', 'Spanish (Spain)', 'Spanish (Spain)'),
    ('zh_CN', 'Simplified Chinese', 'Simplified Chinese'),
    ('zh_TW', 'Traditional Chinese', 'Traditional Chinese'),
    ('ko_KR', 'Korean', 'Korean'),
    ('ru_RU', 'Russian', 'Russian'),
    ('uk_UA', 'Ukrainian', 'Ukrainian'),
    ('cs_CZ', 'Czech', 'Czech'),
    ('pl_PL', 'Polish', 'Polish'),
    ('tr_TR', 'Turkish', 'Turkish'),
    ('ar_EG', 'Arabic', 'Arabic'),
    ('hi_IN', 'Hindi', 'Hindi'),
    ('vi_VN', 'Vietnamese', 'Vietnamese'),
    ('th_TH', 'Thai', 'Thai'),
    ('nl_NL', 'Dutch', 'Dutch'),
    ('sv_SE', 'Swedish', 'Swedish'),
    ('id_ID', 'Indonesian', 'Indonesian'),
    ('sk_SK', 'Slovak', 'Slovak'),
]

NAME_GEN_ITEMS = [
    ('LANG_1', 'Language 1', 'Use Language 1 for object and workspace names'),
    ('LANG_2', 'Language 2', 'Use Language 2 for object and workspace names'),
    ('INDEPENDENT', 'Language Independent', 'Do not translate new data names (Always English)'),
]

def get_addon_name():
    return __package__ if __package__ else __name__

class SwitchLanguagePreferences(bpy.types.AddonPreferences):
    bl_idname = get_addon_name()

    is_initialized: bpy.props.BoolProperty(default=False, options={'HIDDEN'})

    lang_1: bpy.props.EnumProperty(
        name="1st lang", description="First language to switch",
        items=LANG_ITEMS, default='en_US'
    )
    
    lang_2: bpy.props.EnumProperty(
        name="2nd lang", description="Second language to switch",
        items=LANG_ITEMS, default='ja_JP'
    )

    name_gen_lang: bpy.props.EnumProperty(
        name="Name Generation", description="Select how to generate new data names",
        items=NAME_GEN_ITEMS, default='LANG_1'
    )

    show_notification: bpy.props.BoolProperty(
        name="Show Notification", description="Show a notification in the status bar",
        default=True
    )

    show_topbar_button: bpy.props.BoolProperty(
        name="Show Topbar Button", description="Show an icon button in the top menu bar",
        default=True
    )

    def draw(self, context):
        layout = self.layout
        
        row = layout.row(align=True)
        row.prop(self, "lang_1")

        row = layout.row(align=True)
        row.prop(self, "lang_2")
        
        layout.prop(self, "name_gen_lang")
        
        row = layout.row(align=True)
        row.prop(self, "show_notification")
        row.prop(self, "show_topbar_button")
        
        layout.separator()
        layout.label(text="Shortcut Key Setup:")
        
        wm = context.window_manager
        kc = wm.keyconfigs.user
        if kc:
            km = kc.keymaps.get('Window')
            if km:
                kmi = next((item for item in km.keymap_items if item.idname == "wm.switch_language"), None)
                if kmi:
                    layout.context_pointer_set("keymap", km)
                    rna_keymap_ui.draw_kmi(["ADDON", "USER", "DEFAULT"], kc, km, kmi, layout, 0)

class WM_OT_switch_language(bpy.types.Operator):
    bl_idname = "wm.switch_language"
    bl_label = "Switch Language"
    bl_description = "Switch between the two selected languages"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        addon_name = get_addon_name()
        addon_prefs = context.preferences.addons.get(addon_name)
        
        if not addon_prefs:
            self.report({'ERROR'}, "Add-on preferences not found.")
            return {'CANCELLED'}
            
        prefs = addon_prefs.preferences
        view = context.preferences.view
        current_lang = view.language
        
        if hasattr(view, "use_translate_interface") and not view.use_translate_interface:
            view.use_translate_interface = True
        
        next_lang = prefs.lang_2 if current_lang == prefs.lang_1 else prefs.lang_1
        view.language = next_lang
        
        if hasattr(view, "use_translate_new_datanames"):
            if prefs.name_gen_lang == 'INDEPENDENT':
                view.use_translate_new_datanames = False
            else:
                target_lang_code = prefs.lang_1 if prefs.name_gen_lang == 'LANG_1' else prefs.lang_2
                view.use_translate_new_datanames = (target_lang_code != 'en_US')
            
        if prefs.show_notification:
            lang_label = next((item[1] for item in LANG_ITEMS if item[0] == next_lang), next_lang)
            self.report({'INFO'}, f"Language switched -> {lang_label}")
            
        for area in context.screen.areas:
            area.tag_redraw()
            
        return {'FINISHED'}

def draw_topbar(self, context):
    if context.region.alignment != 'RIGHT':
        return
        
    addon_name = get_addon_name()
    addon_prefs = context.preferences.addons.get(addon_name)
    if addon_prefs and addon_prefs.preferences.show_topbar_button:
        self.layout.operator(WM_OT_switch_language.bl_idname, text="", icon='WORLD')

def init_addon_state():
    try:
        addon_name = get_addon_name()
        addon_prefs = bpy.context.preferences.addons.get(addon_name)
        if addon_prefs:
            prefs = addon_prefs.preferences
            if not prefs.is_initialized:
                view = bpy.context.preferences.view
                current_lang = view.language
                
                valid_langs = [item[0] for item in LANG_ITEMS]
                prefs.lang_1 = current_lang if current_lang in valid_langs else 'en_US'
                prefs.lang_2 = 'ja_JP' if prefs.lang_1 == 'en_US' else 'en_US'
                prefs.is_initialized = True
    except Exception:
        pass
    return None

addon_keymaps = []

def register():
    bpy.utils.register_class(SwitchLanguagePreferences)
    bpy.utils.register_class(WM_OT_switch_language)
    bpy.types.TOPBAR_HT_upper_bar.append(draw_topbar)
    bpy.app.timers.register(init_addon_state, first_interval=0.1)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Window', space_type='EMPTY')
        kmi = km.keymap_items.new(WM_OT_switch_language.bl_idname, 'L', 'PRESS', ctrl=True, alt=True)
        addon_keymaps.append((km, kmi))

def unregister():
    bpy.types.TOPBAR_HT_upper_bar.remove(draw_topbar)
    bpy.utils.unregister_class(WM_OT_switch_language)
    bpy.utils.unregister_class(SwitchLanguagePreferences)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()