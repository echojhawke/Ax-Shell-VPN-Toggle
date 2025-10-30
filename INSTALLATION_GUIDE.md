# VPN Button Installation Guide

## Overview
The VPN Toggle Button will add a vpn toggle switcher to your quick settings in Ax-Shell. This will support as many VPNs as you have configured in networkmanager.
Your VPN button matches the styling of the Network and Bluetooth buttons, using the theme's CSS variables and patterns 

## Installation Steps

### 1. Add VPN Icons to `modules/icons.py`

Open `~/.config/Ax-Shell/modules/icons.py` and add these lines:

```python
# VPN Icons using Google Material Icons
vpn_off = "<span font='Material Symbols Outlined'>&#xe593;</span>"  # e593
vpn_on = "<span font='Material Symbols Outlined'>&#xf686;</span>"   # f686
vpn_connected = "<span font='Material Symbols Outlined'>&#xf686;</span>"  # f686
vpn_disconnected = "<span font='Material Symbols Outlined'>&#xe9d4;</span>"  # e9d4
refresh = "<span font='Material Symbols Outlined'>&#xe5d5;</span>"  # refresh icon
```

### 2. Copy Module Files

```bash
# Navigate to your config directory
cd ~/.config/Ax-Shell

# Backup existing files
cp modules/buttons.py modules/buttons.py.backup
cp modules/widgets.py modules/widgets.py.backup

# Copy new files
cp /path/to/vpn_button.py modules/
cp /path/to/vpn_popup.py modules/
cp /path/to/buttons.py modules/
cp /path/to/widgets.py modules/
```

### 3. Add CSS Styling

Open your `buttons.css` file (or wherever you keep button styles) and add the VPN styles.

**Location:** `~/.config/Ax-Shell/styles/buttons.css` (or your equivalent)

Copy and paste the entire contents of `vpn_button_styles.css` at the end of your buttons.css file.

The styles are organized in the same pattern as your existing Network/Bluetooth buttons:
```css
/* === VPN Button Styling === */
#vpn-button { ... }
#vpn-status-button { ... }
#vpn-menu-button { ... }
/* etc. */
```

### 4. Restart Your Application

```bash
# Kill the current instance
pkill -f ax-shell

# Restart (your method may vary)
GTK_DEBUG=interactive uwsm-app $(python /home/[user]/.config/Ax-Shell/main.py)
```

## File Structure After Installation

```
~/.config/Ax-Shell/
├── modules/
│   ├── vpn_button.py      ← NEW: Split button component
│   ├── vpn_popup.py       ← NEW: Popup with device slots
│   ├── buttons.py         ← UPDATED: Imports vpn_button
│   ├── widgets.py         ← UPDATED: Initializes vpn_popup
│   └── icons.py           ← UPDATED: Add VPN icons (Broken)
└── styles/
    └── buttons.css        ← UPDATED: Add VPN styles
```

## Visual States

### 1. VPN Disconnected (Disabled)
```
┌────────────────┬────┐
│  🔑  VPN       │  › │  ← Grey background (var(--surface))
│     Disabled   │    │  ← Grey text (var(--outline))
└────────────────┴────┘
```

### 2. VPN Connected (Active)
```
┌────────────────┬────┐
│  🔒  VPN       │  › │  ← Accent background (var(--primary))
│     DVPN1      │    │  ← Dark text (var(--shadow))
└────────────────┴────┘
```

### 3. Hover State
```
┌────────────────┬────┐
│  🔒  VPN       │  › │  ← Lighter background (var(--foreground))
│     DVPN1      │    │
└────────────────┴────┘
```

## VPN Popup States

### Connection Slot (Disconnected)
```
┌─────────────────────────────────┐
│ 🔑 DVPN1          🔓  [Connect] │  ← Grey button
└─────────────────────────────────┘
```

### Connection Slot (Connected)
```
┌─────────────────────────────────┐
│ 🔑 DVPN1      🔒  [Disconnect]  │  ← Accent color button
└─────────────────────────────────┘
```

### Hover to Disconnect
```
┌─────────────────────────────────┐
│ 🔑 DVPN1      🔒  [Disconnect]  │  ← Red/error color
└─────────────────────────────────┘
```

## Key Features

### Main Button Behavior
1. **Click left side** → Toggles last connected VPN
2. **Click arrow** → Opens VPN applet
3. **Auto-updates** → Every 3 seconds

### VPN Applet Features
1. **Individual controls** → Connect/disconnect each VPN separately
2. **Status indicators** → Visual icons show connection state
3. **Back button** → Return to notification history
4. **Refresh button** → Manually update status
5. **Auto-refresh** → Every 5 seconds

## CSS Customization

If you want to adjust colors or styling:

### Change Active Color
```css
#vpn-status-button {
  background-color: var(--primary);  /* Change this */
}
```

### Change Disabled Color
```css
#vpn-status-button.disabled {
  background-color: var(--surface);  /* Or this */
}
```

### Change Border Radius
```css
#vpn-button {
  border-radius: 16px;  /* Adjust to match your theme */
}
```

### Change Button Height
```css
#vpn-button {
  min-height: 52px;  /* Match other buttons */
}
```

## Troubleshooting

### Icons Show as Boxes
**Problem:** Material Icons not loaded  
**Solution:**
1. Check font is installed: `fc-list | grep Material`
2. Install if missing: `sudo pacman -S ttf-material-symbols-variable`
3. Update font cache: `fc-cache -fv`

### Button Not Colored
**Problem:** CSS not applied  
**Solution:**
1. Check CSS file is loaded
2. Verify selectors match: `#vpn-button`, `#vpn-status-button`, etc.
3. Check for typos in CSS
4. Try adding `!important` temporarily for testing

### VPN Won't Toggle
**Problem:** NetworkManager permissions or connection names  
**Solution:**
1. Test manually: `nmcli con up DVPN1`
2. Check connection exists: `nmcli con show`
3. Verify exact names (case-sensitive)
4. Check NetworkManager is running: `systemctl status NetworkManager`

### Wrong VPN Names
**Problem:** Your VPNs aren't named DVPN1/DVPN2  
**Solution:** Edit `vpn_popup.py` around line 123:
```python
self.dvpn1_slot = VpnConnectionSlot("YOUR_VPN_NAME_1")
self.dvpn2_slot = VpnConnectionSlot("YOUR_VPN_NAME_2")
```

Also update `vpn_button.py` around line 91:
```python
any_up = any(p in active for p in ("YOUR_VPN_NAME_1", "YOUR_VPN_NAME_2"))
```

### Styling Doesn't Match
**Problem:** CSS variables are different in your theme  
**Solution:** Check your theme's variables and adjust:
```css
/* Your theme might use different variable names */
background-color: var(--your-primary-color);
color: var(--your-text-color);
```

## Testing Checklist

After installation, verify:

- [ ] Icons display (not boxes)
- [ ] Button matches Network/Bluetooth style
- [ ] Colors match when VPN connects
- [ ] Colors match when VPN disconnects
- [ ] Hover effects work
- [ ] Main button toggles VPN
- [ ] Arrow opens popup
- [ ] Popup shows both VPNs
- [ ] Connect buttons work
- [ ] Disconnect buttons work
- [ ] Status updates automatically
- [ ] Back button works
- [ ] Refresh button works

## Advanced Customization

### Add More VPNs

In `vpn_popup.py`, add more slots:
```python
self.dvpn3_slot = VpnConnectionSlot("DVPN3")
self.vpn_box.add(self.dvpn3_slot)
```

In `vpn_button.py`, update the check:
```python
any_up = any(p in active for p in ("DVPN1", "DVPN2", "DVPN3"))
```

### Change Update Intervals

**Main Button (default: 3 seconds):**
```python
# In vpn_button.py, line ~131
GLib.timeout_add_seconds(5, self._refresh)  # Change to 5 seconds
```

**Popup (default: 5 seconds):**
```python
# In vpn_popup.py, line ~140
GLib.timeout_add_seconds(10, self.refresh_connections)  # Change to 10 seconds
```

### Customize Button Text

In `vpn_button.py`:
```python
self.vpn_label = Label(
    name="vpn-label",
    label="VPN",  # Change this text
    justification="left",
)
```

## Support

If you encounter issues:

1. **Check console output** for Python errors
2. **Verify file paths** are correct
3. **Test NetworkManager** manually
4. **Check CSS selectors** match your theme
5. **Ensure fonts are installed**

Common commands for debugging:
```bash
# Check VPN connections
nmcli con show

# Test manual connection
nmcli con up DVPN1

# Check NetworkManager status
systemctl status NetworkManager

# View application logs
journalctl -f -u your-app-name

# Check if fonts are available
fc-list | grep Material
```

## What's Next?

Once installed, you can:
- Quickly toggle VPNs from the panel
- Manage multiple VPNs independently
- See connection status at a glance
- Enjoy consistent styling across all buttons

The VPN button now perfectly matches your theme! 🎉
