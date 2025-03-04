from modules.checkpath import checkpath
from configuration.settings import *

def save_user_choices(self, config_file, yuzu_path=None, mode=None):
    log.info(f"Saving user choices in {localconfig}")
    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)

    if mode == "Cheats":
        config["Cheats"] = {}
        for option_name, option_var in self.selected_cheats.items():
            config['Cheats'][option_name] = option_var.get()
        with open(config_file, 'w') as file:
            config["Manager"] = {}
            config["Manager"]["Cheat_Version"] = self.cheat_version.get()
            config.write(file)
        return

    # Save the selected options
    if not config.has_section("Options"):
        config["Options"] = {}
    config['Options']['DFPS Version'] = self.DFPS_var.get()
    config['Options']['Resolution'] = self.resolution_var.get()
    config['Options']['Aspect Ratio'] = self.aspect_ratio_var.get()
    config['Options']['FPS'] = self.fps_var.get()
    config['Options']['ShadowResolution'] = self.shadow_resolution_var.get()
    config['Options']['CameraQuality'] = self.camera_var.get()
    config['Options']['UI'] = self.ui_var.get()
    config['Options']['First Person'] = self.fp_var.get()

    # Save the enable/disable choices
    for option_name, option_var in self.selected_options.items():
        config['Options'][option_name] = option_var.get()

    # Save the yuzu.exe path if provided
    if not config.has_section("Paths"):
        config["Paths"] = {}
    if self.mode == "Yuzu":
        if yuzu_path:
            config['Paths']['YuzuPath'] = yuzu_path
    if self.mode == "Ryujinx":
        if yuzu_path:
            config['Paths']['RyujinxPath'] = yuzu_path

    # Save the manager selected mode I.E Ryujinx/Yuzu
    config["Mode"] = {"ManagerMode": self.mode}
    log.info("User choices saved in Memory,"
             "Attempting to write into file.")
    # Write the updated configuration back to the file
    with open(config_file, 'w') as file:
        config.write(file)
    log.info("Successfully written into log file")


def load_user_choices(self, config_file, mode=None):
    config = configparser.ConfigParser()
    config.read(config_file)

    if mode == "Cheats":
        self.cheat_version.set(config.get("Manager", "Cheat_Version", fallback="Version - 1.2.0"))
        try:
            for option_name, option_var in self.selected_cheats.items():
                option_value = config.get('Cheats', option_name, fallback="Off")
                option_var.set(option_value)
        except AttributeError as e:
            # continue, not important.
            handle = e
        return

    # Load the selected options
    self.cheat_version.set(config.get("Manager", "Cheat_Version", fallback="Version - 1.2.0"))
    self.DFPS_var.set(config.get('Options', 'DFPS Version', fallback="Latest"))
    self.resolution_var.set(config.get('Options', 'Resolution', fallback=self.dfps_options.get("ResolutionNames", [""])[2]))
    self.aspect_ratio_var.set(config.get('Options', 'Aspect Ratio', fallback=AR_list[0]))
    self.fps_var.set(config.get('Options', 'FPS', fallback=str(self.dfps_options.get("FPS", [])[2])))
    self.shadow_resolution_var.set(config.get('Options', 'ShadowResolution', fallback=self.dfps_options.get("ShadowResolutionNames", [""])[0])) # Shadow Auto
    self.camera_var.set(config.get('Options', 'CameraQuality', fallback=self.dfps_options.get("CameraQualityNames", [""])[0]))
    self.ui_var.set(config.get('Options', 'UI', fallback="None"))
    self.fp_var.set(config.get('Options', 'First Person', fallback="Off"))
    # Load the enable/disable choices
    for option_name, option_var in self.selected_options.items():
        option_value = config.get('Options', option_name, fallback="Off")
        option_var.set(option_value)

    # Load the enable/disabled cheats
    try:
        for option_name, option_var in self.selected_cheats.items():
            option_value = config.get('Cheats', option_name, fallback="Off")
            option_var.set(option_value)
    except AttributeError as e:
        # continue, not important.
        handle = e
