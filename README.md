# Ax-Shell VPN Toggle

<img width="1099" height="475" alt="image" src="https://github.com/user-attachments/assets/baf80b41-2587-4c89-8239-b6c1874269e9" />


### Key Features

1. **Split Button Design** 
   - Main button: Quick toggle for last connected VPN
   - Arrow button: Opens detailed VPN applet

2. **Smart Styling**
   - **Active**: Accent color (like WiFi/Bluetooth when connected)
   - **Inactive**: Muted grey (like WiFi/Bluetooth when disabled)
   - **Hover**: Subtle highlight effect

3. **VPN Applet**
   - Bluetooth-style device slots for each VPN
   - Individual connect/disconnect buttons
   - Color-coded status indicators
   - Clean, outlined design matching Bluetooth devices

4. **Google Material Icons**
   - Main button: `e593` (vpn_key)
   - Connected: `f686` (vpn_lock)
   - Disconnected: `e9d4` (vpn_key_off)

## Files Provided

1. **vpn_button.py** - New split button component
2. **vpn_popup.py** - Updated popup with device slots
3. **buttons.py** - Updated to use new VPN button
4. **widgets.py** - Updated to properly initialize VPN popup
5. **icons_vpn_additions.py** - Icon definitions to add
6. **vpn_styling.css** - Complete CSS styling
7. **INSTALLATION_GUIDE.md** - Detailed setup instructions

## Quick Install

```bash
# 1. Add VPN icons to modules/icons.py (see icons_vpn_additions.py)
# 2. Copy new files
cp vpn_button.py ~/.config/Ax-Shell/modules/
cp vpn_popup.py ~/.config/Ax-Shell/modules/
cp buttons.py ~/.config/Ax-Shell/modules/
cp widgets.py ~/.config/Ax-Shell/modules/

# WARNING THIS WILL OVERWRITE ANY EXISTING CUSTOM FILES. BACK UP YOUR FILES FIRST

# 3. Add CSS from vpn_styling.css to your style.css
# 4. Restart your application
```

## How It Works

### Main Button
- **Single Click**: Toggles your last connected VPN (or DVPN1 if first use)
- **Shows**: Current VPN name when connected, "Disabled" when not
- **Updates**: Every 3 seconds automatically

### Arrow Button  
- **Click**: Opens the VPN applet
- **Shows**: All available VPNs with individual controls

### VPN Applet
- **DVPN1 & DVPN2** shown in separate slots
- Each has a **Connect/Disconnect** button
- Buttons change color based on state:
  - Grey when disconnected
  - Accent color when connected
  - Red on hover when connected (to disconnect)

## Testing Checklist

- [ ] VPN icons display correctly
- [ ] Button changes color when VPN connects
- [ ] Main button toggles VPN
- [ ] Arrow opens VPN applet
- [ ] Both VPNs shown in applet
- [ ] Connect/disconnect buttons work
- [ ] Styling matches Bluetooth button
- [ ] Hover effects working

## Troubleshooting Quick Tips

**Icons are boxes?**
→ Add the icon definitions from `icons_vpn_additions.py` to your `modules/icons.py`

**Button not changing color?**
→ Add the CSS from `vpn_styling.css` to your main CSS file

**Can't toggle VPN?**
→ Test manually: `nmcli con up DVPN1`

**Import errors?**
→ Make sure all files are in `~/.config/Ax-Shell/modules/`

---

**Ready to install?** See [INSTALLATION_GUIDE.md](https://github.com/echojhawke/Ax-Shell-VPN-Toggle/blob/main/INSTALLATION_GUIDE.md) for detailed instructions!

## SEE LICENSE.MD
