#
# This causes <prev-tab> key do nothing on the first tab (instead of 
# passing the keypress to the application running in the terminal). Ditto 
# for the last tab. This is kinda annoying.
%bcond_with	disable_prev_next_tab_sensitivity_changes
#
Summary:	GNOME Terminal
Summary(pl):	Terminal dla GNOME
Name:		gnome-terminal
Version:	2.11.2
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-terminal/2.11/%{name}-%{version}.tar.bz2
# Source0-md5:	61cb4c49ea465584e0fd35a7209a37f2
Patch0:		%{name}-TERM.patch
Patch1:		%{name}-disable-prev_next-tab-sensitivity-changes.patch
Patch2:		%{name}-desktop.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.10.0
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	gnome-common >= 2.8.0-2
BuildRequires:	gnome-vfs2-devel >= 2.10.0-2
BuildRequires:	intltool
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libgnomeui-devel >= 2.10.0
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.12.0
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	vte-devel >= 0.11.12
BuildRequires:	xft-devel >= 2.1-2
Requires(post,preun):	GConf2
Requires(post,postun):	scrollkeeper
Requires:	libgnomeui >= 2.10.0
Requires:	startup-notification >= 0.8
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

%build
%{__gnome_doc_common}
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
rm -rf $RPM_BUILD_ROOT%{_datadir}/application-registry

%find_lang %{name} --with-gnome --all-name

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
%doc README ChangeLog NEWS TODO AUTHORS
%doc %{_omf_dest_dir}/%{name}
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/schemas/gnome-terminal.schemas
%{_datadir}/%{name}
%{_libdir}/bonobo/servers/*
%{_desktopdir}/*
%{_pixmapsdir}/*
