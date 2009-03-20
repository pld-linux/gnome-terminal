Summary:	GNOME Terminal
Summary(pl.UTF-8):	Terminal dla GNOME
Name:		gnome-terminal
Version:	2.26.0
Release:	2
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-terminal/2.26/%{name}-%{version}.tar.bz2
# Source0-md5:	013e51a2c4dd7dde5db49587952065ae
Patch0:		%{name}-session-restore.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.24.0
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gnome-doc-utils >= 0.14.0
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.12.0
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	vte-devel >= 0.20.0
BuildRequires:	xorg-lib-libSM-devel
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	startup-notification >= 0.8
Requires:	terminfo
Requires:	vte >= 0.20.0
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a terminal thing that isn't finished at all.

%description -l pl.UTF-8
To jest terminal, na razie całkowicie nie dokończony.

%prep
%setup -q
%patch0 -p0

%build
%{__intltoolize}
%{__gnome_doc_common}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-install \
	--disable-scrollkeeper
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 \
	localedir=%{_localedir}

rm -rf $RPM_BUILD_ROOT%{_datadir}/application-registry

%find_lang %{name} --with-gnome --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install gnome-terminal.schemas
%scrollkeeper_update_post

%preun
%gconf_schema_uninstall gnome-terminal.schemas

%postun
%scrollkeeper_update_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gnome-terminal
%{_datadir}/%{name}
%{_desktopdir}/gnome-terminal.desktop
%{_sysconfdir}/gconf/schemas/gnome-terminal.schemas
