# VPN Button Quick Reference Card

## What to Install

```bash
# 1. Copy module files
vpn_button.py    → ~/.config/axyl/modules/
vpn_popup.py     → ~/.config/axyl/modules/
buttons.py       → ~/.config/axyl/modules/
widgets.py       → ~/.config/axyl/modules/

# 2. Update icons.py
# Add VPN icon definitions from icons_vpn_additions.py

# 3. Update CSS
# Add styles from vpn_styling.css to your style.css

# 4. Restart
pkill -f axyl && restart-your-app
```

## Icon Definitions (Add to icons.py)

```python
vpn_off = "<span font='Material Symbols Outlined'>&#xe593;</span>"
vpn_on = "<span font='Material Symbols Outlined'>&#xf686;</span>"
vpn_connected = "<span font='Material Symbols Outlined'>&#xf686;</span>"
vpn_disconnected = "<span font='Material Symbols Outlined'>&#xe9d4;</span>"
refresh = "<span font='Material Symbols Outlined'>&#xe5d5;</span>"
```

## 🎨 Key CSS Classes

```css
#vpn-button              /* Main container */
#vpn-status-button       /* Left toggle button */
#vpn-menu-button         /* Right arrow button */
#vpn-connection          /* VPN slot in popup */
#vpn-connect.connected   /* Connected button state */
.disabled                /* Inactive/grey state */
```

## 📱 User Interaction

| Action | Result |
|--------|--------|
| Click left side | Toggle last VPN |
| Click arrow | Open VPN applet |
| Click "Connect" | Connect to specific VPN |
| Click "Disconnect" | Disconnect VPN |
| Hover any button | Highlight effect |

## 🎨 Visual States

| State | Icon | Color | Status Text |
|-------|------|-------|-------------|
| Disconnected | e593 | Grey | "Disabled" |
| DVPN1 Active | f686 | Accent | "DVPN1" |
| DVPN2 Active | f686 | Accent | "DVPN2" |

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| Box icons | Add icon defs to icons.py |
| No color change | Add CSS styles |
| Can't toggle | Check `nmcli con show` |
| Import errors | Check file locations |
| Wrong VPN names | Edit vpn_popup.py |

## 📝 Customization Points

### Change VPN Names
**File:** `vpn_popup.py`
```python
# Line ~123
self.dvpn1_slot = VpnConnectionSlot("YOUR_VPN_1")
self.dvpn2_slot = VpnConnectionSlot("YOUR_VPN_2")
```

### Add More VPNs
**File:** `vpn_popup.py`
```python
self.dvpn3_slot = VpnConnectionSlot("DVPN3")
self.vpn_box.add(self.dvpn3_slot)
```

### Adjust Update Speed
**File:** `vpn_button.py`
```python
# Line ~131
GLib.timeout_add_seconds(3, self._refresh)  # Change 3
```

### Change Colors
**File:** `style.css`
```css
#vpn-status-button {
    color: @accent;  /* Change accent color */
}
```

## 🧪 Testing Commands

```bash
# List VPN connections
nmcli con show

# Connect manually
nmcli con up DVPN1

# Disconnect manually
nmcli con down DVPN1

# Show active connections
nmcli con show --active

# Check NetworkManager status
systemctl status NetworkManager
```

## 📂 File Structure

```
~/.config/axyl/
├── modules/
│   ├── vpn_button.py      ← New split button
│   ├── vpn_popup.py       ← Updated popup
│   ├── buttons.py         ← Updated imports
│   ├── widgets.py         ← Updated init
│   └── icons.py           ← Add VPN icons
└── style.css              ← Add VPN styles
```

## ✅ Installation Checklist

- [ ] Backed up original files
- [ ] Copied vpn_button.py
- [ ] Copied vpn_popup.py  
- [ ] Updated buttons.py
- [ ] Updated widgets.py
- [ ] Added icons to icons.py
- [ ] Added CSS styles
- [ ] Restarted application
- [ ] Tested VPN toggle
- [ ] Tested VPN applet
- [ ] Verified styling

## 🚀 Expected Behavior

1. **Initial Load**
   - Button shows grey "Disabled" if no VPN active
   - Shows accent color + VPN name if active

2. **Click Main Button**
   - Toggles last used VPN (or DVPN1 first time)
   - Updates within 0.5 seconds
   - Color changes immediately

3. **Click Arrow**
   - Opens VPN applet
   - Shows both VPNs with status
   - Each has individual control

4. **In Applet**
   - Can connect/disconnect either VPN
   - Back button returns to notifications
   - Refresh button updates status
   - Status auto-updates every 5 seconds

## 📞 Support

If issues persist:
1. Check console for Python errors
2. Verify file paths and permissions
3. Test `nmcli` commands manually
4. Ensure NetworkManager is running
5. Check CSS syntax

## 🎉 Features Summary

✓ Split button design (like Bluetooth)
✓ Accent color when active
✓ Grey when inactive  
✓ Quick toggle functionality
✓ Detailed VPN applet
✓ Per-VPN controls
✓ Google Material Icons
✓ Bluetooth-style slots
✓ Auto-updating status
✓ Hover effects

---

**Need detailed instructions?** → See INSTALLATION_GUIDE.md
**Want to see changes?** → See VISUAL_COMPARISON.md
**Quick overview?** → See README.md
