#
# This causes <prev-tab> key do nothing on the first tab (instead of 
# passing the keypress to the application running in the terminal). Ditto 
# for the last tab. This is kinda annoying.
%bcond_with	disable_prev_next_tab_sensitivity_changes
#
Summary:	GNOME Terminal
Summary(pl):	Terminal dla GNOME
Name:		gnome-terminal
Version:	2.10.0
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-terminal/2.10/%{name}-%{version}.tar.bz2
# Source0-md5:	062744daca0c7f708b8c52f47b5db0d1
Patch0:		%{name}-TERM.patch
Patch1:		%{name}-disable-prev_next-tab-sensitivity-changes.patch
Patch2:		%{name}-desktop.patch
Patch3:		%{name}-ne.po.patch
#Patch3:		%{name}-font_smoothing.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.10.0
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	gtk+2-devel >= 2:2.6.0
BuildRequires:	gnome-common >= 2.8.0-2
BuildRequires:	gnome-vfs2-devel >= 2.10.0-2
BuildRequires:	intltool
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libgnomeui-devel >= 2.10.0
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.12.0
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	scrollkeeper
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	vte-devel >= 0.11.12
BuildRequires:	xft-devel >= 2.1-2
Requires(post):	GConf2
Requires(post):	scrollkeeper
Requires:	libgnomeui >= 2.10.0
Requires:	terminfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a terminal thing that isn't finished at all.

%description -l pl
To jest terminal, na razie ca³kowicie nie dokoñczony.

%prep
%setup -q
%patch0 -p1
%if %{with disable_prev_next_tab_sensitivity_changes}
%patch1 -p1
%endif
%patch2 -p1
%patch3 -p1
#%%patch3 -p0

%build
cp /usr/share/gnome-common/data/omf.make .
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
