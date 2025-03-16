#
# Conditional build:
%bcond_without	nautilus	# Nautilus extension
%bcond_without	transparency	# restore transparency feature
%bcond_without	search_provider	# build GNOME Shell search provder

Summary:	GNOME Terminal
Summary(pl.UTF-8):	Terminal dla GNOME
Name:		gnome-terminal
Version:	3.56.0
Release:	1
License:	GPL v3+
Group:		X11/Applications
#SourceDownload: https://gitlab.gnome.org/GNOME/gnome-terminal/-/tags
#Source0:	https://gitlab.gnome.org/GNOME/gnome-terminal/-/archive/%{version}/%{name}-%{version}.tar.bz2
Source0:	https://download.gnome.org/sources/gnome-terminal/3.56/%{name}-%{version}.tar.xz
# Source0-md5:	18b84b3a11b39860d5a130752a586e68
Patch1:		%{name}-transparency.patch
URL:		https://wiki.gnome.org/Apps/Terminal/
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.52.0
%{?with_search_provider:BuildRequires:	gnome-shell-devel >= 3.12.0}
BuildRequires:	gsettings-desktop-schemas-devel >= 0.1.0
BuildRequires:	gtk+3-devel >= 3.22.27
BuildRequires:	libhandy1-devel >= 1.6.0
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libuuid-devel
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.62.0
%{?with_nautilus:BuildRequires:	nautilus-devel >= 43}
BuildRequires:	ninja >= 1.5
BuildRequires:	pcre2-8-devel >= 10.00
BuildRequires:	pkgconfig >= 1:0.12.0
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
BuildRequires:	vte-devel >= 0.80.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	glib2 >= 1:2.52.0
Requires:	glib2 >= 1:2.52.0
Requires:	gsettings-desktop-schemas >= 0.1.0
Requires:	gtk+3 >= 3.22.27
Requires:	libhandy1 >= 1.6.0
Requires:	pcre2-8 >= 10.00
Requires:	terminfo
Requires:	vte >= 0.80.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a terminal thing that isn't finished at all.

%description -l pl.UTF-8
To jest terminal, na razie całkowicie nie dokończony.

%package -n nautilus-extension-terminal
Summary:	GNOME Terminal extension for Nautilus
Summary(pl.UTF-8):	Rozszerzenie GNOME Terminal dla Nautilusa
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus >= 43
Obsoletes:	nautilus-open-terminal < 0.20-2

%description -n nautilus-extension-terminal
This package provides a Nautilus extension that adds the 'Open in
Terminal' option to the right-click context menu in Nautilus.

%description -n nautilus-extension-terminal -l pl.UTF-8
Ten pakiet dostarcza rozszerzenie Nautilusa dodające opcję "Otwórz w
terminalu" do menu kontekstowego uaktywnianego prawym klawiszem myszy
w Nautilusie.

%prep
%setup -q
%{?with_transparency:%patch -P1 -p1}

%build
%meson \
	%{!?with_nautilus:-Dnautilus_extension=false} \
	%{!?with_search_provider:-Dsearch_provider=false}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
if [ "$1" = "0" ]; then
	%glib_compile_schemas
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/gnome-terminal
%attr(755,root,root) %{_libexecdir}/gnome-terminal-preferences
%attr(755,root,root) %{_libexecdir}/gnome-terminal-server
%dir %{_libdir}/gnome-terminal
%{_libdir}/gnome-terminal/gschemas.compiled
%{_datadir}/dbus-1/services/org.gnome.Terminal.service
%{_datadir}/glib-2.0/schemas/org.gnome.Terminal.gschema.xml
%{?with_search_provider:%{_datadir}/gnome-shell/search-providers/gnome-terminal-search-provider.ini}
%{_datadir}/metainfo/org.gnome.Terminal.metainfo.xml
%{_datadir}/xdg-terminals/org.gnome.Terminal.desktop
%{_desktopdir}/org.gnome.Terminal.desktop
%{_desktopdir}/org.gnome.Terminal.Preferences.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Terminal.svg
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Terminal.Preferences.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Terminal-symbolic.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Terminal.Preferences-symbolic.svg
%{systemduserunitdir}/gnome-terminal-server.service
%{_mandir}/man1/gnome-terminal.1*

%if %{with nautilus}
%files -n nautilus-extension-terminal
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus/extensions-4/libterminal-nautilus.so
%{_datadir}/metainfo/org.gnome.Terminal.Nautilus.metainfo.xml
%endif
