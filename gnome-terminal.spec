#
# This causes <prev-tab> key do nothing on the first tab (instead of 
# passing the keypress to the application running in the terminal). Ditto 
# for the last tab. This is kinda annoying.
%bcond_with	disable_prev_next_tab_sensitivity_changes
#
Summary:	GNOME Terminal
Summary(pl):	Terminal dla GNOME
Name:		gnome-terminal
Version:	2.8.0
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/2.8/%{name}-%{version}.tar.bz2
# Source0-md5:	93e59f24b35bd867653664565adb4672
Patch0:		%{name}-TERM.patch
Patch1:		%{name}-disable-prev_next-tab-sensitivity-changes.patch
Patch2:		%{name}-desktop.patch
Patch3:		%{name}-font_smoothing.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.8.0.1
Buildrequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	gtk+2-devel >= 2:2.4.0
Buildrequires:	gnome-vfs2-devel >= 2.8.0
BuildRequires:	intltool
BuildRequires:	libglade2-devel >= 1:2.4.0
BuildRequires:	libgnomeui-devel >= 2.8.0
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 0.12.0
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	scrollkeeper
BuildRequires:	startup-notification-devel >= 0.7
BuildRequires:	vte-devel >= 0.11.11
BuildRequires:	xft-devel >= 2.1-2
Requires(post):	GConf2
Requires(post):	scrollkeeper
Requires:	libgnomeui >= 2.8.0
Requires:	terminfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a terminal thing that isn't finished at all.

%description -l pl
To jest terminal, na razie ca³kowicie nie dokoñczony.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%if %{with disable_prev_next_tab_sensitivity_changes}
%patch2 -p1
%endif
%patch3 -p0

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 \
	localedir=%{_localedir}

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

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
