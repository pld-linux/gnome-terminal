Summary:	GNOME Terminal
Summary(pl):	Terminal dla GNOME
Name:		gnome-terminal
Version:	2.5.1
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/2.5/%{name}-%{version}.tar.bz2
# Source0-md5:	71a9c9a70ca0c6b633944fad358109a8
Patch0:		%{name}-TERM.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.4.0.1
BuildRequires:	gtk+2-devel >= 2.3.1
BuildRequires:	libglade2-devel >= 2.3.1
BuildRequires:	libgnomeui-devel >= 2.5.1
BuildRequires:	pkgconfig >= 0.12.0
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	scrollkeeper
BuildRequires:	startup-notification-devel >= 0.5
BuildRequires:	vte-devel >= 0.11.7
BuildRequires:	xft-devel >= 2.1-2
BuildRequires:	XFree86-OpenGL-devel
Requires(post):	GConf2
Requires(post):	scrollkeeper
Requires:	libgnomeui >= 2.4.0
Requires:	terminfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a terminal thing that isn't finished at all.

%description -l pl
To jest terminal, na razie ca³kowicie nie dokoñczony.

%prep
%setup -q
%patch0 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 \
	localedir=%{_localedir}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/scrollkeeper-update
%gconf_schema_install

%postun	-p /usr/bin/scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog NEWS TODO AUTHORS
%doc %{_omf_dest_dir}/%{name}
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/schemas/*
%{_datadir}/%{name}
%{_libdir}/bonobo/servers/*
%{_desktopdir}/*
%{_pixmapsdir}/*
%{_datadir}/application-registry/*
