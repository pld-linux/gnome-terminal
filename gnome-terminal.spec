Summary:	GNOME Terminal
Summary(pl.UTF-8):	Terminal dla GNOME
Name:		gnome-terminal
Version:	3.8.2
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-terminal/3.8/%{name}-%{version}.tar.xz
# Source0-md5:	90b983f50587f3fbc0de24c99ebe24cc
Patch0:		%{name}-desktop.patch
Patch1:		wordseps.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.32.0
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	dconf-devel >= 0.12
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.33.2
BuildRequires:	gnome-common
BuildRequires:	gsettings-desktop-schemas-devel >= 0.1.0
BuildRequires:	gtk+3-devel >= 3.6.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	libxml2-progs
BuildRequires:	pkgconfig >= 1:0.12.0
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	tar >= 1:1.22
BuildRequires:	vte-devel >= 0.34.0
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	glib2 >= 2.33.2
Requires:	glib2 >= 1:2.33.2
Requires:	gsettings-desktop-schemas >= 0.1.0
Requires:	terminfo
Requires:	vte >= 0.34.0
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a terminal thing that isn't finished at all.

%description -l pl.UTF-8
To jest terminal, na razie całkowicie nie dokończony.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__intltoolize}
%{__gnome_doc_common}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	localedir=%{_localedir}

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
%{_datadir}/dbus-1/services/org.gnome.Terminal.service
%{_datadir}/glib-2.0/schemas/org.gnome.Terminal.gschema.xml
%{_desktopdir}/gnome-terminal.desktop
