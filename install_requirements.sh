#!/bin/bash

# Check for the presence of package manager commands
if command -v apt &> /dev/null; then
    PACKAGE_MANAGER="apt"
elif command -v pacman &> /dev/null; then
    PACKAGE_MANAGER="pacman"
elif command -v dnf &> /dev/null; then
    PACKAGE_MANAGER="dnf"
elif command -v zypper &> /dev/null; then
    PACKAGE_MANAGER="yum"
else
    echo "Unable to determine the package manager"
    exit 1
fi

echo "Package manager: $PACKAGE_MANAGER"

# Install packages based on the package manager
case $PACKAGE_MANAGER in
    "apt")
        sudo apt update
        sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-4.0 bpftrace
        ;;
    "pacman")
        sudo pacman -Syu --noconfirm python-gobject gtk4 bpftrace
        ;;
    "dnf")
        sudo $PACKAGE_MANAGER install -y python3-gobject gtk4 bpftrace
        ;;
    "zypper")
        sudo $PACKAGE_MANAGER install -y python3-gobject python3-gobject-Gdk typelib-1_0-Gtk-4_0 libgtk-4-1 bpftrace
        ;;
    *)
        echo "Unsupported package manager"
        exit 1
        ;;
esac

echo "Packages installed successfully"
