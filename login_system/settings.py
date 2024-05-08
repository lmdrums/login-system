from configparser import RawConfigParser

def make_default_settings_file(settings: 
                               dict[str, dict[str, str | int | float | bool]], 
                               directory: str) -> None:
    config = RawConfigParser()

    for section, section_settings in settings.items():
        config[section] = section_settings

    with open(directory, "w", encoding="utf-8") as file:
        config.write(file)

def edit_setting(section: str, name: str, value: str | int | float | bool, 
                 directory: str) -> None:
    """Edits a setting in the given configuration file."""
    config = RawConfigParser()
    config.read(directory)

    config.set(section, name, str(value))

    with open(directory, "w", encoding="utf-8") as file:
        config.write(file)

def get_setting(directory: str, section: str, 
                name: str, integer: bool=False, 
                floatp: bool=False, boolean: 
                bool=False) -> str | int | float | bool:
    """Gets a certain setting from file"""
    config = RawConfigParser()
    config.read(directory)
    
    c_kwargs = {"section": section, "option": name}

    if integer:
        return config.getint(**c_kwargs)
    if floatp:
        return config.getfloat(**c_kwargs)
    if boolean:
        return config.getboolean(**c_kwargs)

    return config.get(**c_kwargs)