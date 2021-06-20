def unit_markers(units):
    """show unit markers for different unit bases (degrees Celsius vs Farrenheit, etc)"""
    if units=="imperial":
        return ("℉", "mph")
    elif units=="metric":
        return ("℃", "km/h")
    return ("°K", "km/h")
