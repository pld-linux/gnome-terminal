#
# Conditional build:
%bcond_without	nautilus	# Nautilus extension
%bcond_without	transparency

Summary:	GNOME Terminal
Summary(pl.UTF-8):	Terminal dla GNOME
Name:		gnome-terminal
Version:	3.24.0
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-terminal/3.24/%{name}-%{version}.tar.xz
# Source0-md5:	f1b2a3e0d4e7eda8ad5ac6a08742e030
Patch1:		%{name}-transparency.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.32.0
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	dconf-devel >= 0.14
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.42.0
BuildRequires:	gnome-common
BuildRequires:	gnome-shell-devel >= 3.12.0
BuildRequires:	gsettings-desktop-schemas-devel >= 0.1.0
BuildRequires:	gtk+3-devel >= 3.10.0
BuildRequires:	intltool >= 0.50.0
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-progs
%{?with_nautilus:BuildRequires:	nautilus-devel >= 3.0.0}
BuildRequires:	pcre2-8-devel >= 10.00
BuildRequires:	pkgconfig >= 1:0.12.0
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	tar >= 1:1.22
BuildRequires:	vte-devel >= 0.42.1
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	glib2 >= 1:2.42.0
Requires:	dconf >= 0.14
Requires:	glib2 >= 1:2.42.0
Requires:	gsettings-desktop-schemas >= 0.1.0
Requires:	gtk+3 >= 3.10.0
Requires:	terminfo
Requires:	vte >= 0.42.1
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
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
Requires:	nautilus >= 3.0.0
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
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	%{?with_nautilus:--with-nautilus-extension}

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
%attr(755,root,root) %{_libdir}/gnome-terminal-migration
%attr(755,root,root) %{_libdir}/gnome-terminal-server
%{_datadir}/metainfo/org.gnome.Terminal.appdata.xml
%{_datadir}/dbus-1/services/org.gnome.Terminal.service
%{_datadir}/glib-2.0/schemas/org.gnome.Terminal.gschema.xml
%{_datadir}/gnome-shell/search-providers/gnome-terminal-search-provider.ini
%{_desktopdir}/org.gnome.Terminal.desktop
%{systemduserunitdir}/gnome-terminal-server.service

%if %{with nautilus}
%files -n nautilus-extension-terminal
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus/extensions-3.0/libterminal-nautilus.so
%{_datadir}/metainfo/org.gnome.Terminal.Nautilus.metainfo.xml
%endif
