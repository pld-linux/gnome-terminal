#
# Conditional build:
# This causes <prev-tab> key do nothing on the first tab (instead of 
# passing the keypress to the application running in the terminal). Ditto 
# for the last tab. This is kinda annoying.
%bcond_with	disable_prev_next_tab_sensitivity_changes
# This is specific to PLD and causes an "unknown term type" on most other
# hosts I have to work on (the rest of the world uses xterm for g-t)
%bcond_with	term_voodoo
#
Summary:	GNOME Terminal
Summary(pl):	Terminal dla GNOME
Name:		gnome-terminal
Version:	2.16.0
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-terminal/2.16/%{name}-%{version}.tar.bz2
# Source0-md5:	d49b53478d49a813c4ecc2836143bb5d
Patch0:		%{name}-TERM.patch
Patch1:		%{name}-disable-prev_next-tab-sensitivity-changes.patch
Patch2:		%{name}-desktop.patch
Patch3:		%{name}-save-session-crash.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	gtk+2-devel >= 2:2.10.3
BuildRequires:	gnome-common >= 2.12.0
BuildRequires:	gnome-vfs2-devel >= 2.16.0
BuildRequires:	intltool >= 0.35
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libgnomeui-devel >= 2.16.0
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.12.0
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	vte-devel >= 0.14.0
Requires(post,preun):	GConf2 >= 2.14.0
Requires(post,postun):	scrollkeeper
Requires:	libgnomeui >= 2.16.0
Requires:	startup-notification >= 0.8
Requires:	vte >= 0.14.0
Requires:	terminfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a terminal thing that isn't finished at all.

%description -l pl
To jest terminal, na razie ca³kowicie nie dokoñczony.

%prep
%setup -q
%if %{with term_voodoo}
%patch0 -p1
%endif
%if %{with disable_prev_next_tab_sensitivity_changes}
%patch1 -p1
%endif
%patch2 -p1
%patch3 -p1

%build
%{__intltoolize}
%{__gnome_doc_common}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
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
%doc AUTHORS ChangeLog NEWS README
%doc %{_omf_dest_dir}/%{name}
%attr(755,root,root) %{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_datadir}/%{name}
%{_desktopdir}/*
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/gnome-terminal.schemas
