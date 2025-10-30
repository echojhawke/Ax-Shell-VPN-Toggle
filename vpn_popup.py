import subprocess
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from gi.repository import GLib

import modules.icons as icons


class VpnConnectionSlot(CenterBox):
    """Individual VPN connection slot, similar to BluetoothDeviceSlot"""
    
    def __init__(self, vpn_name: str, **kwargs):
        super().__init__(name="vpn-connection", **kwargs)
        self.vpn_name = vpn_name
        
        # Connection status icon
        self.connection_label = Label(
            name="vpn-connection-status",
            markup=icons.vpn_disconnected
        )
        
        # Connect/Disconnect button
        self.connect_button = Button(
            name="vpn-connect",
            label="Connect",
            on_clicked=lambda *_: self.toggle_connection(),
        )
        
        # VPN name and status
        self.start_children = [
            Box(
                spacing=8,
                h_expand=True,
                h_align="fill",
                children=[
                    Label(
                        name="vpn-slot-icon",
                        markup=icons.vpn_off,
                        style_classes=["vpn-slot-icon"]
                    ),
                    Label(
                        label=vpn_name,
                        h_expand=True,
                        h_align="start",
                        ellipsization="end",
                        name="vpn-name-label"
                    ),
                    self.connection_label,
                ],
            )
        ]
        self.end_children = self.connect_button
        
        # Initial state check
        GLib.idle_add(self.check_status)
    
    def toggle_connection(self):
        """Toggle VPN connection"""
        try:
            # Check current status
            active = subprocess.check_output(
                ["nmcli", "-t", "-f", "NAME", "con", "show", "--active"],
                text=True,
            ).splitlines()
            
            if self.vpn_name in active:
                # Disconnect
                subprocess.run(["nmcli", "con", "down", self.vpn_name], check=False)
            else:
                # Connect
                subprocess.run(["nmcli", "con", "up", self.vpn_name], check=False)
            
            # Update status after a short delay
            GLib.timeout_add(500, self.check_status)
        except Exception as e:
            print(f"VPN toggle error for {self.vpn_name}: {e}")
    
    def check_status(self):
        """Check and update connection status"""
        try:
            active = subprocess.check_output(
                ["nmcli", "-t", "-f", "NAME", "con", "show", "--active"],
                text=True,
            ).splitlines()
            
            is_connected = self.vpn_name in active
            
            # Update connection icon
            self.connection_label.set_markup(
                icons.vpn_connected if is_connected else icons.vpn_disconnected
            )
            
            # Update button
            self.connect_button.set_label("Disconnect" if is_connected else "Connect")
            
            # Update button style
            if is_connected:
                self.connect_button.add_style_class("connected")
            else:
                self.connect_button.remove_style_class("connected")
        except Exception as e:
            print(f"VPN status check error for {self.vpn_name}: {e}")
        
        return False


class VpnPopup(Box):
    """VPN connections popup, similar to BluetoothConnections"""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="vpn-popup",
            spacing=4,
            orientation="vertical",
            **kwargs,
        )
        
        # Back button to return to notifications
        self.back_button = Button(
            name="vpn-back",
            child=Label(name="vpn-back-label", markup=icons.chevron_left),
            on_clicked=lambda *_: self.show_notif_callback() if hasattr(self, 'show_notif_callback') else None
        )
        
        # Refresh button
        self.refresh_label = Label(name="vpn-refresh-label", markup=icons.refresh)
        self.refresh_button = Button(
            name="vpn-refresh",
            child=self.refresh_label,
            tooltip_text="Refresh VPN status",
            on_clicked=lambda *_: self.refresh_connections()
        )
        
        # VPN connection slots container
        self.vpn_box = Box(spacing=2, orientation="vertical")
        
        # Create slots for DVPN1 and DVPN2
        self.dvpn1_slot = VpnConnectionSlot("DVPN1")
        self.dvpn2_slot = VpnConnectionSlot("DVPN2")
        
        self.vpn_box.add(self.dvpn1_slot)
        self.vpn_box.add(self.dvpn2_slot)
        
        # Build the UI
        self.children = [
            CenterBox(
                name="vpn-header",
                start_children=self.back_button,
                center_children=Label(name="vpn-text", label="VPN Connections"),
                end_children=self.refresh_button
            ),
            ScrolledWindow(
                name="vpn-connections",
                min_content_size=(-1, -1),
                child=self.vpn_box,
                v_expand=True,
                propagate_width=False,
                propagate_height=False,
            ),
        ]
        
        # Start periodic refresh
        GLib.timeout_add_seconds(5, self.refresh_connections)
    
    def set_widgets_instance(self, widgets):
        """Set reference to widgets instance for navigation"""
        self.widgets = widgets
        self.show_notif_callback = widgets.show_notif
    
    def refresh_connections(self):
        """Refresh status of all VPN connections"""
        self.dvpn1_slot.check_status()
        self.dvpn2_slot.check_status()
        return True
