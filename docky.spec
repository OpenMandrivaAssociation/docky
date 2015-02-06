%global         debug_package %{nil}

Name:           docky
Version:        2.1.4
Release:        2
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
BuildRequires:  libGConf2-devel
BuildRequires:  gio-sharp-devel
BuildRequires:  dbus-sharp-devel dbus-sharp-glib-devel
# native deps
BuildRequires:  glib2-devel gtk2-devel
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
#patch0 -p1
#patch1 -p1


%build
%configure
make %{?_smp_mflags}


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


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


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





%changelog

* Fri Jan 11 2013 umeabot <umeabot> 2.1.4-2.mga3
+ Revision: 349053
- Mass Rebuild - https://wiki.mageia.org/en/Feature:Mageia3MassRebuild

* Sat Jul 28 2012 malo <malo> 2.1.4-1.mga3
+ Revision: 275408
- update to version 2.1.4

* Sat Jan 28 2012 malo <malo> 2.1.3-1.mga2
+ Revision: 202747
- new version 2.1.3
- updated files and dependencies
- dropped patches

* Sat Jan 28 2012 malo <malo> 2.0.12-1.mga2
+ Revision: 202742
- fix devel group
- spec clean-up after import from Fedora.
- imported package docky

