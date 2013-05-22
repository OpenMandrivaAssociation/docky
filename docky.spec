%global         debug_package %{nil}

Name:           docky
Version:        2.1.4
Release:        3
Summary:        Advanced shortcut bar written in Mono

Group:          Graphical desktop/GNOME
License:        GPLv3+
URL:            http://wiki.go-docky.com
Source0:        http://launchpad.net/docky/2.1/%{version}/+download/docky-%{version}.tar.xz

Requires:       gnome-sharp2 gnome-desktop-sharp
Requires:       gnome-keyring-sharp mono-addins
Requires:       mono ndesk-dbus notify-sharp gtk2
Requires:       hicolor-icon-theme
Requires:       gio-sharp 
Requires:       dbus-sharp dbus-sharp-glib

# sharp deps
BuildRequires:  gnome-sharp2-devel gnome-desktop-sharp-devel
BuildRequires:  gnome-keyring-sharp gtk-sharp2-devel mono-addins-devel
BuildRequires:  mono-devel ndesk-dbus-devel ndesk-dbus-glib-devel
BuildRequires:  notify-sharp-devel
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  gio-sharp-devel
BuildRequires:  dbus-sharp-devel pkgconfig(dbus-sharp-glib-1.0)
# native deps
BuildRequires:  pkgconfig(glib-2.0) pkgconfig(gtk+-2.0)
BuildRequires:  gettext
BuildRequires:  perl-XML-Parser
BuildRequires:  intltool
BuildRequires:  desktop-file-utils

# Mono only available on these:
ExclusiveArch: %ix86 x86_64 ppc ppc64 ia64 %{arm} sparcv9 alpha s390x


%description
Docky is an advanced shortcut bar that sits at the bottom, top, and/or sides 
of your screen. It provides easy access to some of the files, folders, 
and applications on your computer, displays which applications are 
currently running, holds windows in their minimized state, and more.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files
for developing applications that use %{name}.


%prep
%setup -q


%build
%configure2_5x
%make


%install
make install DESTDIR=$RPM_BUILD_ROOT

#gapi_codegen.exe is not distributed (licence is GNU GPL v2)
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/gapi_codegen*

desktop-file-install    \
        --dir $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart       \
        --add-only-show-in=GNOME                                \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
desktop-file-install --delete-original  \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        --remove-category Application \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

# autostart is disabled by default
echo "X-GNOME-Autostart-enabled=false" >> \
    $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/%{name}.desktop

%find_lang %{name}


%files -f %{name}.lang
%doc AUTHORS COPYING COPYRIGHT NEWS
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/icons/hicolor/*/apps/gmail.png
%{_datadir}/icons/hicolor/*/mimetypes/*
%{_datadir}/applications/*.desktop
%config(noreplace) %{_sysconfdir}/xdg/autostart/%{name}.desktop
%{_sysconfdir}/gconf/schemas/docky.schemas
%doc %{_mandir}/man1/%{name}.1*


%files devel
%{_libdir}/pkgconfig/docky.cairohelper.pc
%{_libdir}/pkgconfig/docky.services.pc
%{_libdir}/pkgconfig/docky.widgets.pc
%{_libdir}/pkgconfig/docky.items.pc

