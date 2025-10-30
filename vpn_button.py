import subprocess
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.label import Label
from gi.repository import GLib
import modules.icons as icons


def add_hover_cursor(widget):
    from gi.repository import Gdk
    widget.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)
    widget.connect("enter-notify-event", lambda w, e: w.get_window().set_cursor(Gdk.Cursor.new_from_name(w.get_display(), "pointer")) if w.get_window() else None)
    widget.connect("leave-notify-event", lambda w, e: w.get_window().set_cursor(None) if w.get_window() else None)


class VpnButton(Box):
    """
    VPN button similar to Bluetooth, with:
    - Main button that toggles last-used VPN
    - Menu button (arrow) that opens the VPN applet
    """
    
    def __init__(self, **kwargs):
        self.widgets_instance = kwargs.pop("widgets")
        
        # Create icon and labels
        self.vpn_icon = Label(
            name="vpn-icon",
            markup=icons.vpn_off,  # Will be updated to use e593
        )
        self.vpn_label = Label(
            name="vpn-label",
            label="VPN",
            justification="left",
        )
        self.vpn_label_box = Box(children=[self.vpn_label, Box(h_expand=True)])
        self.vpn_status_text = Label(
            name="vpn-status",
            label="Disabled",
            justification="left",
        )
        self.vpn_status_box = Box(children=[self.vpn_status_text, Box(h_expand=True)])
        
        self.vpn_text = Box(
            name="vpn-text",
            orientation="v",
            h_align="start",
            v_align="center",
            children=[self.vpn_label_box, self.vpn_status_box],
        )
        
        self.vpn_status_content = Box(
            h_align="start",
            v_align="center",
            spacing=10,
            children=[self.vpn_icon, self.vpn_text],
        )
        
        # Main status button - toggles last VPN
        self.vpn_status_button = Button(
            name="vpn-status-button",
            h_expand=True,
            child=self.vpn_status_content,
            on_clicked=lambda *_: self.toggle_last_vpn(),
        )
        add_hover_cursor(self.vpn_status_button)
        
        # Menu button - opens VPN applet
        self.vpn_menu_label = Label(
            name="vpn-menu-label",
            markup=icons.chevron_right,
        )
        self.vpn_menu_button = Button(
            name="vpn-menu-button",
            child=self.vpn_menu_label,
            on_clicked=lambda *_: self.widgets_instance.notch.open_notch("vpn"),
        )
        add_hover_cursor(self.vpn_menu_button)
        
        super().__init__(
            name="vpn-button",
            orientation="h",
            h_align="fill",
            v_align="fill",
            h_expand=True,
            v_expand=True,
            spacing=0,
            children=[self.vpn_status_button, self.vpn_menu_button],
        )
        
        self.widgets_list = [
            self, self.vpn_icon, self.vpn_label,
            self.vpn_status_text, self.vpn_status_button,
            self.vpn_menu_button, self.vpn_menu_label
        ]
        
        self.last_vpn = None  # Track last connected VPN
        
        # Start periodic refresh
        GLib.timeout_add_seconds(3, self._refresh)
        GLib.idle_add(self._refresh)
    
    def toggle_last_vpn(self):
        """Toggle the last connected VPN or connect to first available"""
        try:
            # Get active connections
            active = subprocess.check_output(
                ["nmcli", "-t", "-f", "NAME", "con", "show", "--active"],
                text=True,
            ).splitlines()
            
            # Check if any VPN is active
            if "DVPN1" in active:
                # Disconnect DVPN1
                subprocess.run(["nmcli", "con", "down", "DVPN1"], check=False)
                self.last_vpn = "DVPN1"
            elif "DVPN2" in active:
                # Disconnect DVPN2
                subprocess.run(["nmcli", "con", "down", "DVPN2"], check=False)
                self.last_vpn = "DVPN2"
            else:
                # No VPN active, connect to last used or DVPN1
                vpn_to_connect = self.last_vpn or "DVPN1"
                subprocess.run(["nmcli", "con", "up", vpn_to_connect], check=False)
                self.last_vpn = vpn_to_connect
            
            # Immediate refresh
            GLib.timeout_add(500, self._refresh)
        except Exception as e:
            print(f"VPN toggle error: {e}")
    
    def _refresh(self):
        """Update button state based on active VPN connections"""
        try:
            active = subprocess.check_output(
                ["nmcli", "-t", "-f", "NAME", "con", "show", "--active"],
                text=True,
            ).splitlines()
        except subprocess.CalledProcessError:
            active = []
        
        # Check which VPN is active
        dvpn1_active = "DVPN1" in active
        dvpn2_active = "DVPN2" in active
        any_vpn_active = dvpn1_active or dvpn2_active
        
        # Update icon based on status
        if any_vpn_active:
            self.vpn_icon.set_markup(icons.vpn_on)
            # Remove disabled style
            for widget in self.widgets_list:
                widget.remove_style_class("disabled")
            
            # Update status text
            if dvpn1_active:
                self.vpn_status_text.set_label("DVPN1")
                self.last_vpn = "DVPN1"
            elif dvpn2_active:
                self.vpn_status_text.set_label("DVPN2")
                self.last_vpn = "DVPN2"
        else:
            self.vpn_icon.set_markup(icons.vpn_off)
            # Add disabled style
            for widget in self.widgets_list:
                widget.add_style_class("disabled")
            self.vpn_status_text.set_label("Disabled")
        
        return True
