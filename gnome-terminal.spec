#
# Conditional build:
%bcond_without	nautilus	# Nautilus extension
%bcond_without	transparency	# restore transparency feature

Summary:	GNOME Terminal
Summary(pl.UTF-8):	Terminal dla GNOME
Name:		gnome-terminal
Version:	3.38.3
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-terminal/3.38/%{name}-%{version}.tar.xz
# Source0-md5:	cef7deb6780f493a4c510cef3984c34f
Patch1:		%{name}-transparency.patch
URL:		https://wiki.gnome.org/Apps/Terminal/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	dconf-devel >= 0.14
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.52.0
BuildRequires:	gnome-shell-devel >= 3.12.0
BuildRequires:	gsettings-desktop-schemas-devel >= 0.1.0
BuildRequires:	gtk+3-devel >= 3.22.27
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-progs
%{?with_nautilus:BuildRequires:	nautilus-devel >= 3.28.0}
BuildRequires:	pcre2-8-devel >= 10.00
BuildRequires:	pkgconfig >= 1:0.12.0
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	tar >= 1:1.22
BuildRequires:	vte-devel >= 0.62.1
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	glib2 >= 1:2.52.0
Requires:	dconf >= 0.14
Requires:	glib2 >= 1:2.52.0
Requires:	gsettings-desktop-schemas >= 0.1.0
Requires:	gtk+3 >= 3.22.27
Requires:	terminfo
Requires:	vte >= 0.62.1
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
Requires:	nautilus >= 3.28.0
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
%{?with_transparency:%patch1 -p1}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	%{!?with_nautilus:--without-nautilus-extension}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	localedir=%{_localedir}

%if %{with nautilus}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-3.0/libterminal-nautilus.la
%endif

%find_lang %{name} --with-gnome --all-name

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
%doc AUTHORS ChangeLog NEWS
%attr(755,root,root) %{_bindir}/gnome-terminal
%attr(755,root,root) %{_libexecdir}/gnome-terminal-server
%{_datadir}/dbus-1/services/org.gnome.Terminal.service
%{_datadir}/glib-2.0/schemas/org.gnome.Terminal.gschema.xml
%{_datadir}/gnome-shell/search-providers/gnome-terminal-search-provider.ini
%{_datadir}/metainfo/org.gnome.Terminal.appdata.xml
%{_desktopdir}/org.gnome.Terminal.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Terminal.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Terminal-symbolic.svg
%{systemduserunitdir}/gnome-terminal-server.service
%{_mandir}/man1/gnome-terminal.1*

%if %{with nautilus}
%files -n nautilus-extension-terminal
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus/extensions-3.0/libterminal-nautilus.so
%{_datadir}/metainfo/org.gnome.Terminal.Nautilus.metainfo.xml
%endif
